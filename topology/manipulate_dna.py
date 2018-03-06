# deal with namings
import os
from Bio.PDB import PDBParser
# Load things
P = PDBParser()

# Parse PDB and run DSSP
pdbf_path = os.path.abspath('lildna.pdb')
dna_model = P.get_structure('dna_model', pdbf_path)

bp_ref = {'THY': 'T', 'GUA': 'G', 'CYT': 'C', 'ADE': 'A'}

for residue in dna_model.get_residues():
	residue.resname = bp_ref[residue.resname]