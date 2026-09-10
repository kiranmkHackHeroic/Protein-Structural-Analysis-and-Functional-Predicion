# 🧬 Protein Structural Analysis and Functional Prediction

A state-of-the-art computational biology platform integrating real-time UniProt sequence retrieval, RCSB PDB 3D structural rendering, Guruprasad DIWV biochemical stability prediction, multi-species ortholog alignment, protein-protein interaction networks, and clinical disease-drug mapping into a single, high-performance web dashboard.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Repository Structure](#-repository-structure)
- [Quick Start](#-quick-start)
  - [Option A: Python Flask Backend (Recommended)](#option-a-python-flask-backend-recommended)
  - [Option B: Direct Browser Launch](#option-b-direct-browser-launch)
  - [Option C: Command-Line Analysis Pipeline](#option-c-command-line-analysis-pipeline)
- [REST API Endpoints](#-rest-api-endpoints)
- [The 24 Curated Master Proteins](#-the-24-curated-master-proteins)
- [Scientific Algorithms & Methodology](#-scientific-algorithms--methodology)
- [Demo & Presentation Guide](#-demo--presentation-guide)
- [Scientific References](#-scientific-references)
- [License](#-license)

---

## 📋 Overview

Traditional bioinformatics workflows require researchers to manually navigate between disjoint databases (UniProt for sequences, RCSB PDB for coordinates, STRING for interaction networks, ClinVar/OMIM for clinical variants, and PubChem for drug discovery).

**This platform bridges that gap by unifying sequence analysis, atomic 3D structure visualization, and clinical translation into one interface:**
- ⚡ **Zero-Friction Analysis**: Enter any valid UniProt Accession ID (e.g., `P69905`, `P04637`, `P04626`) or click any pre-analyzed protein to load complete structural and biochemical profiles instantly.
- 🌐 **Live Database Sync with Offline Resilience**: Queries live REST APIs (UniProtKB and RCSB PDB) with an embedded 24-protein cache for instant offline fallback.
- 🔬 **Clinical Relevance**: Directly links structural mutations (e.g., Hemoglobin E6V, p53 R248W, BRCA1 185delAG) to real patient diseases and FDA-approved therapeutics.

---

## 🌟 Key Features

| Feature | Description | Biological Significance |
|:---|:---|:---|
| **Interactive 3D Molecular Viewer** | WebGL-powered 3D visualization using `3Dmol.js` with cartoon, stick, and sphere styles, rotation controls, and camera reset | Inspect active sites, secondary structure elements, and binding clefts |
| **Biochemical Property Profiling** | Molecular weight, isoelectric point (pI), aromaticity, and secondary structure fractions (helix, sheet, turn) | Predicts charge states, purification parameters, and physical properties |
| **Guruprasad DIWV Stability Index** | Implements the 400-dipeptide weight value algorithm (Guruprasad et al., 1990) | Classifies proteins as **Stable** ($<40$), **Moderately Stable** ($40-50$), or **Unstable** ($>50$) |
| **Multi-Species Ortholog Alignment** | Compares human target against chimpanzee, mouse, chicken, zebrafish, and yeast orthologs | High conservation ($>70\%$) pinpoints evolutionarily constrained, indispensable functional motifs |
| **Protein-Protein Interaction Network** | Mapped functional binding partners categorized by strength (*Critical*, *Essential*, *Functional*, *Moderate*) | Reveals multi-protein complexes, allosteric regulators, and signaling cascades |
| **Disease & Genetic Mutation Mapping** | Documents clinical disorders, Mendelian inheritance modes, specific amino acid alterations, and global prevalence | Connects primary sequence changes directly to human pathology |
| **Therapeutic & Drug Discovery Impact** | Outlines real FDA-approved drugs (e.g., Voxelotor, Herceptin, Olaparib, Osimertinib, Humira) | Illustrates how atomic structural insights translate to clinical pharmacology |

---

## 🏗️ System Architecture

```
                      +------------------------------------------+
                      |         Web Browser Frontend             |
                      |        (protein_analyzer.html)           |
                      +--------------------+---------------------+
                                           |
                    +----------------------+----------------------+
                    |                                             |
            [Local REST API]                              [External APIs]
                    |                                             |
                    v                                             v
        +-----------------------+                    +------------------------+
        |   Flask Server        |                    |  UniProt REST API      |
        |   (app.py:8080)       |                    |  (rest.uniprot.org)    |
        +-----------+-----------+                    +-----------+------------+
                    |                                             |
                    v                                             v
        +-----------------------+                    +------------------------+
        |  BioPython Engine     |                    |  RCSB PDB API          |
        |  - ProtParam          |                    |  (files.rcsb.org)      |
        |  - PDBIO / PDBParser  |                    |  (data.rcsb.org)       |
        +-----------+-----------+                    +-----------+------------+
                    |                                             |
                    +----------------------+----------------------+
                                           |
                                           v
                             +---------------------------+
                             |    Interactive Output     |
                             |  - 3D Structure (3Dmol)   |
                             |  - Stability & Properties |
                             |  - Ortholog Alignment     |
                             |  - Interaction Networks   |
                             |  - Disease & Drug Mapping |
                             +---------------------------+
```

---

## 📁 Repository Structure

```
Protein-Structural-Analysis-and-Functional-Predicion-main/
├── app.py                      # Flask backend API server & static file host
├── bio.py                      # Standalone CLI protein analysis script
├── protein_analyzer.html       # Full single-page interactive dashboard with 3Dmol.js
├── README.md                   # Comprehensive documentation & reference guide
├── DEMO_CHEAT_SHEET.txt        # Word-for-word presentation script and timing guide
├── DEMO_PREPARATION.md         # Demonstration rehearsal, Q&A, and contingency guide
├── FINAL_CHECKLIST.txt         # Pre-demo verification and feature checklist
├── LICENSE                     # MIT Open Source License
└── results/
    ├── all_proteins_data.json  # Complete 24-protein pre-computed master dataset
    ├── analysis_results.json   # Exported analysis results from bio.py execution
    └── HBA_1A3N_chainA.pdb     # Sample crystallographic chain coordinates
```

---

## 🚀 Quick Start

### Option A: Python Flask Backend (Recommended)

Running the Flask backend provides access to both the web dashboard and the full REST API:

```bash
# 1. Install required dependencies
python3 -m pip install flask flask-cors biopython requests urllib3

# 2. Start the application server
python3 app.py
```

Open your browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

---

### Option B: Direct Browser Launch

The application is completely self-contained. You can open the HTML file directly in any modern web browser without running a server:

```bash
# macOS
open protein_analyzer.html

# Linux
xdg-open protein_analyzer.html

# Windows
start protein_analyzer.html
```

---

### Option C: Command-Line Analysis Pipeline

Use `bio.py` to analyze any protein via UniProt ID from the terminal:

```bash
# Analyze default protein (Hemoglobin alpha - P69905)
python3 bio.py

# Analyze a specific protein by UniProt accession (e.g., HER2 / ERBB2)
python3 bio.py P04626

# Output is automatically formatted and saved to results/analysis_results.json
```

---

## 🔌 REST API Endpoints

When running `app.py`, the following REST API endpoints are active on port `8080`:

### `GET /api/proteins`
Returns the master catalog of all 24 pre-analyzed proteins with metadata, categories, and PDB associations.

**Example Request:**
```bash
curl -s http://localhost:8080/api/proteins
```

---

### `POST /api/analyze`
Submits a protein UniProt ID for complete biochemical analysis, sequence processing, PDB structure fetching, and disease mapping.

**Request Payload:**
```json
{
  "uniprot_id": "P04637"
}
```

**Example Request:**
```bash
curl -X POST http://localhost:8080/api/analyze \
     -H "Content-Type: application/json" \
     -d '{"uniprot_id": "P04637"}'
```

**Sample Response:**
```json
{
  "uniprot_id": "P04637",
  "protein_name": "P53_HUMAN",
  "description": "Cellular tumor antigen p53",
  "organism": "Homo sapiens",
  "analysis": {
    "sequence_length": 393,
    "molecular_weight": 43652.71,
    "isoelectric_point": 6.33,
    "aromaticity": 0.0611,
    "instability_index": 73.59,
    "stability": "Unstable",
    "secondary_structure": {
      "helix": 30.0,
      "sheet": 35.6,
      "turn": 26.5
    }
  },
  "pdb_id": "1TUP",
  "diseases": [
    {
      "disease": "Li-Fraumeni Syndrome (LFS)",
      "inheritance": "Autosomal Dominant",
      "mutation": "Germline TP53 mutations (R175H, R248Q, R273H)",
      "treatment": "Surveillance MRI, early surgical intervention"
    }
  ]
}
```

---

## 🧬 The 24 Curated Master Proteins

The platform features 24 comprehensively documented proteins organized into 6 biological categories:

### 1. Featured & Essential Proteins
| UniProt ID | Symbol | Protein Name | PDB ID | Primary Clinical Focus | Approved Therapeutics |
|:---|:---|:---|:---|:---|:---|
| **P69905** | `HBA1` | Hemoglobin subunit alpha | `1A3N` | Sickle cell disease, $\alpha$-thalassemia | Voxelotor, Casgevy (CRISPR), Hydroxyurea |
| **P01308** | `INS` | Insulin | `4AIY` | Type 1 & 2 diabetes mellitus | Lispro, Aspart, Glargine, Degludec |
| **P04637** | `TP53` | Cellular tumor antigen p53 | `1TUP` | 50% of all human cancers, Li-Fraumeni | APR-246 (Eprenetapopt), Nutlin-3 |
| **P04626** | `ERBB2` | HER2 / Receptor tyrosine kinase erbB-2 | `1N8Z` | HER2+ breast & gastric adenocarcinoma | Trastuzumab (Herceptin), Enhertu (T-DXd) |
| **P38398** | `BRCA1` | Breast cancer type 1 susceptibility protein | `1JM7` | Hereditary Breast & Ovarian Cancer (HBOC) | Olaparib (Lynparza), Talazoparib |
| **Q9BYF1** | `ACE2` | Angiotensin-converting enzyme 2 | `6M0J` | SARS-CoV-2 (COVID-19), hypertension | Paxlovid, mRNA-1273, BNT162b2 |
| **P00533** | `EGFR` | Epidermal growth factor receptor | `1M17` | Non-small cell lung cancer (NSCLC) | Osimertinib (Tagrisso), Gefitinib |

### 2. Cancer & Tumor Biology
| UniProt ID | Symbol | Protein Name | PDB ID | Primary Clinical Focus | Approved Therapeutics |
|:---|:---|:---|:---|:---|:---|
| **P12931** | `SRC` | Proto-oncogene tyrosine kinase Src | `2SRC` | Metastatic colon & prostate cancer | Dasatinib (Sprycel), Bosutinib |
| **P42212** | `TNF` | Tumor necrosis factor ($\text{TNF}-\alpha$) | `1TNF` | Rheumatoid arthritis, Crohn's disease | Adalimumab (Humira), Etanercept |
| **O75015** | `TP73` | Tumor protein p73 | `2XWC` | Neuroblastoma, backup tumor suppressor | Itch inhibitors, cisplatin synergy |

### 3. Metabolic & Endocrine
| UniProt ID | Symbol | Protein Name | PDB ID | Primary Clinical Focus | Approved Therapeutics |
|:---|:---|:---|:---|:---|:---|
| **P02649** | `APOB` | Apolipoprotein B-100 | `2L5C` | Familial hypercholesterolemia, ASCVD | Statins, Ezetimibe, Mipomersen |
| **P35367** | `PPARG` | Peroxisome proliferator-activated receptor $\gamma$ | `2PRG` | Type 2 diabetes, insulin resistance | Pioglitazone (Actos), Rosiglitazone |
| **P51449** | `SOD2` | Superoxide dismutase [Mn], mitochondrial | `1VAR` | Dilated cardiomyopathy, oxidative stress | Avasopasem manganese, MitoQ |
| **P00698** | `LYZ` | Lysozyme C | `1HEL` | Innate bacterial mucosal defense | Historic 1st enzyme crystal structure (1965) |

### 4. Cell Signaling & Transcription
| UniProt ID | Symbol | Protein Name | PDB ID | Primary Clinical Focus | Approved Therapeutics |
|:---|:---|:---|:---|:---|:---|
| **P35556** | `DLL1` | Delta-like protein 1 (Notch ligand) | `4XBM` | Spondylocostal dysostosis, somite clock | Stem cell expansion matrices |
| **P31431** | `RELA` | Transcription factor p65 (NF-$\kappa\text{B}$) | `1NFI` | Multiple myeloma, chronic inflammation | Bortezomib (Velcade), Dexamethasone |
| **Q92846** | `SMAD3` | Mothers against decapentaplegic homolog 3 | `1MJS` | Loeys-Dietz syndrome, tissue fibrosis | Losartan, Pirfenidone |

### 5. DNA Repair & Proteostasis
| UniProt ID | Symbol | Protein Name | PDB ID | Primary Clinical Focus | Approved Therapeutics |
|:---|:---|:---|:---|:---|:---|
| **P63104** | `UBB` | Ubiquitin | `1UBQ` | 26S proteasome degradation, neurodegeneration | PROTAC degraders, Lenalidomide |
| **P25398** | `TXNRD1` | Thioredoxin reductase 1, cytoplasmic | `2ZZ0` | Chemotherapy-resistant tumors | Auranofin (Ridaura gold complex) |

### 6. Oxygen Transport & Structural Architecture
| UniProt ID | Symbol | Protein Name | PDB ID | Primary Clinical Focus | Approved Therapeutics |
|:---|:---|:---|:---|:---|:---|
| **P02144** | `MB` | Myoglobin | `1MBO` | Acute myocardial infarction biomarker | Historic 1st protein crystal structure (1958) |
| **P99999** | `CYCS` | Cytochrome c | `1HRC` | Mitochondrial electron chain & apoptosis | Venetoclax (Venclexta), molecular clock |
| **P02768** | `ALB` | Serum albumin | `1AO6` | Hypoalbuminemia, oncotic pressure, drug carrier | Abraxane (nab-Paclitaxel), 20% Albumin |
| **P08100** | `RHO` | Rhodopsin | `1F88` | Retinitis pigmentosa, night blindness | Historic 1st GPCR crystal structure (2000) |
| **P02452** | `COL1A1` | Collagen alpha-1(I) chain | `1CAG` | Osteogenesis imperfecta, Ehlers-Danlos | Integra regenerative dermal templates |

---

## 🔬 Scientific Algorithms & Methodology

### 1. DIWV Stability Index (Guruprasad et al., 1990)
The instability index predicts whether a protein will be stable in vitro based on its dipeptide composition:

$$\text{II} = \frac{10}{L} \sum_{i=1}^{L-1} \text{DIWV}(x_i, x_{i+1})$$

Where:
- $L$ is the sequence length
- $\text{DIWV}(x_i, x_{i+1})$ is the instability weight value assigned to the dipeptide pair formed by residue $x_i$ and $x_{i+1}$ (across a $20 \times 20 = 400$ matrix)
- **Classification Thresholds**:
  - $\text{II} < 40$: **Stable** (extended half-life in solution)
  - $40 \le \text{II} < 50$: **Moderately Stable**
  - $\text{II} \ge 50$: **Unstable** (requires chaperone stabilization or short physiological turnover)

### 2. Isoelectric Point ($\text{pI}$) Calculation
Determines the pH at which the net electrical charge of the protein is exactly zero by iteratively solving the Henderson-Hasselbalch charge balance equation across all ionizable groups ($\text{N-terminus}$, $\text{C-terminus}$, $\text{Asp}$, $\text{Glu}$, $\text{Cys}$, $\text{Tyr}$, $\text{His}$, $\text{Lys}$, $\text{Arg}$).

### 3. Aromaticity Analysis
Measures the relative frequency of aromatic residues (Phenylalanine $\text{Phe}$, Tyrosine $\text{Tyr}$, and Tryptophan $\text{Trp}$):

$$\text{Aromaticity} = \frac{N_{\text{Phe}} + N_{\text{Tyr}} + N_{\text{Trp}}}{L}$$

Aromaticity is closely correlated with ultraviolet absorbance at $280\text{ nm}$ ($A_{280}$) and hydrophobic core stabilization.

---

## 🎓 Demo & Presentation Guide

For academic presentations, thesis defenses, or professor demonstrations, refer to the included cheat sheets:
- **[DEMO_CHEAT_SHEET.txt](file:///Users/kiranmk/Downloads/Protein-Structural-Analysis-and-Functional-Predicion-main/DEMO_CHEAT_SHEET.txt)**: Minute-by-minute talking points.
- **[DEMO_PREPARATION.md](file:///Users/kiranmk/Downloads/Protein-Structural-Analysis-and-Functional-Predicion-main/DEMO_PREPARATION.md)**: Rehearsal checklist and expected Q&A.

### Recommended 3-Step Demo Progression:
1. **Hemoglobin (`P69905`)**:
   - Point to the DIWV index ($6.97 \rightarrow \text{Extremely Stable}$).
   - Show how a single mutation ($\text{Glu6Val}$) distorts erythrocytes and affects 100M people.
   - Show how structural biology guided **Voxelotor** to inhibit polymerization.
2. **p53 (`P04637`)**:
   - Explain the "Guardian of the Genome" role and its instability index ($73.59$).
   - Discuss how p53 is mutated in $>50\%$ of human cancers.
   - Highlight small-molecule refolding drug **APR-246**.
3. **HER2 (`P04626`)** or **ACE2 (`Q9BYF1`)**:
   - Demonstrate antibody-drug conjugates (**Enhertu**) or the Spike-binding interface of COVID-19.

---

## 📚 Scientific References

1. **DIWV Stability Index**: Guruprasad, K., Reddy, B. V., & Pandit, M. W. (1990). Correlation between stability of a protein and its dipeptide composition. *Protein Engineering, Design and Selection*, 4(2), 155–161.
2. **UniProt Knowledgebase**: The UniProt Consortium (2023). UniProt: the Universal Protein Knowledgebase in 2023. *Nucleic Acids Research*, 51(D1), D523–D531.
3. **RCSB Protein Data Bank**: Burley, S. K., et al. (2021). RCSB Protein Data Bank: powerful new tools for exploring 3D structures. *Nucleic Acids Research*, 49(D1), D437–D451.
4. **3Dmol.js WebGL Engine**: Nicholas, R., & Koes, D. (2015). 3Dmol.js: molecular visualization with WebGL. *Bioinformatics*, 31(8), 1322–1324.
5. **BioPython**: Cock, P. A., et al. (2009). Biopython: freely available Python tools for computational molecular biology and bioinformatics. *Bioinformatics*, 25(11), 1422–1423.

---

## 📄 License

This project is open-source and licensed under the [MIT License](file:///Users/kiranmk/Downloads/Protein-Structural-Analysis-and-Functional-Predicion-main/LICENSE).
