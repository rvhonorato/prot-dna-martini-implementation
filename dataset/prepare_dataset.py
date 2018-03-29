# prepare the dataset, convert residue names?

from Bio.PDB import PDBParser
from Bio.PDB import PDBIO
from Bio.PDB.StructureBuilder import StructureBuilder

dna_nuc = {
	'CYT': 'DC',
	'THY': 'DT',
	'ADE': 'DA',
	'GUA': 'DG'
}

pdb = '1A74_complex.pdb'


# Load things
P = PDBParser()
io = PDBIO()

aa_model = P.get_structure('complex_model', pdb)
exit()
for model in aa_model:
	for chain in model:
		for r in chain.get_residues():
			if r.resname in dna_nuc.keys():
				# rename!
				r.resname = dna_nuc[r.resname]

# rewrite
structure_builder=StructureBuilder()
structure_builder.init_structure("converted_complex_model")
structure_builder.init_seg(' ') # Empty SEGID

for model in aa_model:
	structure_builder.init_model(model.id)
	for chain in model:
		structure_builder.init_chain(chain.id)
		for residue in chain:
			structure_builder.init_residue(residue.resname, residue.id[0], residue.id[1], residue.id[2])
			for atom in residue:
				structure_builder.init_atom(
					atom.name, 
					atom.coord, 
					atom.bfactor, 
					atom.occupancy, 
					atom.altloc, 
					atom.fullname,
					element=atom.element
					)

converted_structure = structure_builder.get_structure()

# Write coarse grained structure
io.set_structure(converted_structure)
io.save('%s-edit.pdb' % (pdb.split('.pdb')[0]), write_end=1)
				