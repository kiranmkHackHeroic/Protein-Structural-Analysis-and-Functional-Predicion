from Bio import ExPASy, SwissProt
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.Blast import NCBIWWW
from Bio.PDB.PDBList import PDBList
from Bio.PDB.PDBParser import PDBParser
import requests
import re
import os
import io
import urllib.error
import ssl
import json

# ----- SETUP -----
uniprot_id = "P69905"   # Hemoglobin alpha
print("Fetching sequence from UniProt...")

# ----- SEQUENCE RETRIEVAL -----
try:
    handle = ExPASy.get_sprot_raw(uniprot_id)
    record = SwissProt.read(handle)
    sequence = record.sequence
except (urllib.error.URLError, ssl.SSLCertVerificationError, Exception):
    # Fall back to requests if there's an SSL/cert verification issue
    import urllib3
    urllib3.disable_warnings()
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"
    resp = requests.get(url, verify=False, timeout=30)
    resp.raise_for_status()
    handle = io.StringIO(resp.text)
    record = SwissProt.read(handle)
    sequence = record.sequence
print("Sequence length:", len(sequence))

# ----- BIOCHEMICAL ANALYSIS -----
analysis = ProteinAnalysis(sequence)
print("\n--- BIOCHEMICAL PROPERTIES ---")
print("Molecular Weight:", analysis.molecular_weight())
print("Isoelectric Point:", analysis.isoelectric_point())
print("Aromaticity:", analysis.aromaticity())
print("Instability Index:", analysis.instability_index())
print("Secondary Structure Fraction:", analysis.secondary_structure_fraction())

# ----- MOTIF SEARCH -----
print("\n--- MOTIF SEARCH ---")
motif = r"N[^P][ST]"  # N-glycosylation motif
matches = list(re.finditer(motif, sequence))
for m in matches:
    print("Motif found at:", m.start())

# ----- DOMAIN PREDICTION -----
print("\n--- DOMAIN PREDICTION FROM PFAM ---")
url = f"https://pfam.xfam.org/protein/{record.accessions[0]}?output=json"
try:
    import urllib3
    urllib3.disable_warnings()
    resp = requests.get(url, verify=False, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    for r in data.get("regions", []):
        print("Domain:", r.get("type"), "from", r.get("start"), "to", r.get("end"))
except Exception as e:
    print(f"Warning: Could not fetch PFAM data ({type(e).__name__}); skipping domain prediction.")

# ----- BLAST SEARCH -----
print("\nRunning BLAST search... this may take 2 minutes...")
os.makedirs("results", exist_ok=True)
try:
    result = NCBIWWW.qblast("blastp", "nr", sequence)
    with open("results/blast.xml", "w") as f:
        f.write(result.read())
    print("BLAST results saved to results/blast.xml")
except Exception:
    print("Warning: BLAST search failed (likely SSL/network issue); skipping BLAST step.")

# ----- PDB STRUCTURE DOWNLOAD -----
print("\nDownloading 3D structure from PDB...")
try:
    pdbl = PDBList()
    pdbl.retrieve_pdb_file("1A3N", pdir="data", file_format="pdb")

    # ----- PARSE STRUCTURE -----
    print("\n--- PDB STRUCTURE PARSING ---")
    parser = PDBParser()
    os.makedirs("data", exist_ok=True)
    structure = parser.get_structure("hb", "data/pdb1a3n.ent")

    if structure:
        for model in structure:
            for chain in model:
                print("Chain:", chain.id)
except Exception:
    print("Warning: Could not download or parse PDB structure; skipping PDB analysis.")

print("\nAnalysis complete!")

# ----- EXPORT RESULTS TO JSON -----
print("\nExporting results to JSON...")
os.makedirs("results", exist_ok=True)

secondary_structure = analysis.secondary_structure_fraction()
results = {
    "uniprot_id": uniprot_id,
    "sequence_length": len(sequence),
    "molecular_weight": analysis.molecular_weight(),
    "isoelectric_point": analysis.isoelectric_point(),
    "aromaticity": analysis.aromaticity(),
    "instability_index": analysis.instability_index(),
    "secondary_structure": {
        "helix": secondary_structure[0],
        "sheet": secondary_structure[1],
        "turn": secondary_structure[2]
    }
}

with open("results/analysis_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Results exported to results/analysis_results.json")
