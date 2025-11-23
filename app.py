from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from Bio import ExPASy, SwissProt
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.PDB.PDBList import PDBList
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.PDBIO import PDBIO, Select
import requests
import os
import io
import tempfile
import ssl
import urllib.error

app = Flask(__name__, static_folder='.')
CORS(app)

# Disable SSL warnings
import urllib3
urllib3.disable_warnings()

class ChainSelect(Select):
    def __init__(self, chain_id):
        self.chain_id = chain_id
    
    def accept_chain(self, chain):
        return chain.id == self.chain_id

def fetch_sequence(uniprot_id):
    """Fetch protein sequence from UniProt"""
    try:
        handle = ExPASy.get_sprot_raw(uniprot_id)
        record = SwissProt.read(handle)
        return record.sequence, record
    except (urllib.error.URLError, ssl.SSLCertVerificationError, Exception):
        # Fallback to requests with SSL verification disabled
        url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"
        resp = requests.get(url, verify=False, timeout=30)
        resp.raise_for_status()
        handle = io.StringIO(resp.text)
        record = SwissProt.read(handle)
        return record.sequence, record

def analyze_protein(sequence):
    """Perform biochemical analysis on protein sequence"""
    analysis = ProteinAnalysis(sequence)
    
    secondary_structure = analysis.secondary_structure_fraction()
    instability = analysis.instability_index()
    
    return {
        "sequence_length": len(sequence),
        "molecular_weight": round(analysis.molecular_weight(), 2),
        "isoelectric_point": round(analysis.isoelectric_point(), 2),
        "aromaticity": round(analysis.aromaticity(), 4),
        "instability_index": round(instability, 2),
        "stability": "Stable" if instability < 40 else "Unstable",
        "secondary_structure": {
            "helix": round(secondary_structure[0] * 100, 1),
            "sheet": round(secondary_structure[1] * 100, 1),
            "turn": round(secondary_structure[2] * 100, 1)
        }
    }

def fetch_pdb_structure(uniprot_id):
    """Fetch PDB structure for UniProt ID"""
    try:
        # Query UniProt for PDB cross-references
        url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}?format=json"
        resp = requests.get(url, verify=False, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        # Find PDB references
        pdbs = [db for db in data.get('uniProtKBCrossReferences', []) if db.get('database') == 'PDB']
        
        if not pdbs:
            return None, "No PDB structure found"
        
        # Get first PDB ID
        pdb_id = pdbs[0].get('id')
        
        # Download PDB file
        pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
        pdb_resp = requests.get(pdb_url, verify=False, timeout=30)
        pdb_resp.raise_for_status()
        
        # Parse and extract first protein chain
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as tmp:
            tmp.write(pdb_resp.text)
            tmp_path = tmp.name
        
        try:
            parser = PDBParser(QUIET=True)
            structure = parser.get_structure(pdb_id, tmp_path)
            
            # Find first protein chain
            target_chain = None
            if structure:
                for model in structure:
                    for chain in model:
                        has_aa = False
                        for res in chain:
                            if res.get_id()[0] == ' ':
                                has_aa = True
                                break
                        if has_aa:
                            target_chain = chain.id
                            break
                    if target_chain:
                        break
            
            if not target_chain:
                return None, "No protein chain found in PDB"
            
            # Save chain to string
            io_handler = PDBIO()
            io_handler.set_structure(structure)
            
            output = io.StringIO()
            io_handler.save(output, ChainSelect(target_chain))
            pdb_content = output.getvalue()
            
            os.unlink(tmp_path)
            
            return pdb_content, pdb_id
            
        except Exception as e:
            os.unlink(tmp_path)
            return None, f"Error parsing PDB: {str(e)}"
            
    except Exception as e:
        return None, f"Error fetching PDB: {str(e)}"

@app.route('/')
def index():
    return send_from_directory('.', 'webapp.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze protein by UniProt ID"""
    try:
        data = request.json if request.json else {}
        uniprot_id = data.get('uniprot_id', '').strip().upper()
        
        if not uniprot_id:
            return jsonify({'error': 'UniProt ID is required'}), 400
        
        # Fetch sequence
        try:
            sequence, record = fetch_sequence(uniprot_id)
        except Exception as e:
            return jsonify({'error': f'Invalid UniProt ID or fetch failed: {str(e)}'}), 400
        
        # Analyze protein
        analysis_results = analyze_protein(str(sequence))
        
        # Fetch PDB structure
        pdb_content, pdb_info = fetch_pdb_structure(uniprot_id)
        
        response = {
            'uniprot_id': uniprot_id,
            'protein_name': record.entry_name if record and hasattr(record, 'entry_name') else 'Unknown',
            'description': record.description if record and hasattr(record, 'description') else 'No description',
            'organism': record.organism if record and hasattr(record, 'organism') else 'Unknown',
            'sequence': str(sequence),
            'analysis': analysis_results,
            'pdb_structure': pdb_content,
            'pdb_id': pdb_info if pdb_content else None,
            'pdb_error': pdb_info if not pdb_content else None
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
