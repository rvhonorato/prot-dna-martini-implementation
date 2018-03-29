# given a protein complex, extract its chains and generate the tbl file
import sys, os

from Bio.PDB import PDBParser
from Bio.PDB import PDBIO
from Bio.PDB.StructureBuilder import StructureBuilder

def get_anchor(r):
	if 'CA' in r.child_dict.keys():
		atom = 'CA'
	elif 'P' in r.child_dict.keys():
		atom = 'P'
	else:
		atom = None
	return atom


P = PDBParser()
io = PDBIO()


pdbf = sys.argv[1]
pdb_name = pdbf.split('.pdb')[0]

structure = P.get_structure(pdb_name, pdbf)

structure_builder=StructureBuilder()
# structure_builder.init_structure("cg_model")
# structure_builder.init_seg(' ') # Empty SEGID

target_chains = [c for c in sys.argv[2:]]
# chainA = 'A'
# chainB = 'B'

selected_structures = {}
for model in structure:
	for chain in model:
		if chain.id in target_chains:
			structure_builder.init_structure("name_%s" % chain.id)
			structure_builder.init_seg(chain.id)
			structure_builder.init_model(model.id)
			structure_builder.init_chain(chain.id)

			for residue in chain:
				if residue.id[0] != ' ': # filter HETATMS
					continue
				structure_builder.init_residue(residue.resname, residue.id[0], residue.id[1], residue.id[2])
				for atom in residue:
					structure_builder.init_atom(atom.name, atom.coord, atom.bfactor,atom.occupancy,atom.altloc,atom.fullname,serial_number=None, element=atom.element)
					# init_atom(name, coord, b_factor, occupancy, altloc, fullname, serial_number=None, element=None)
			selected = structure_builder.get_structure()
			io.set_structure(selected)
			io.save('%s_%s.pdb' % (pdb_name, chain.id), write_end=1)
			selected_structures[chain.id] = '%s_%s.pdb' % (pdb_name, chain.id)
			#
			# convert to CG
			#
			# os.system('python ~/Nostromo/aa2cg/aa2cg-prot_dna.py %s_%s.pdb' % (pdb_name, chain.id))


# os.system('cat %s > %s_%s.pdb' % (' '.join(selected_structures.values()), pdb_name, ''.join(selected_structures.keys())))
# os.system('python ~/Nostromo/aa2cg/aa2cg-prot_dna.py %s_%s.pdb' % (pdb_name, ''.join(selected_structures.keys())))

interface_dic = dict([(c, []) for c in target_chains])

# generate combinations and check interfaces..!
dist_threshold = 4.
import itertools
c = 0
for chainA_idx, chainB_idx in itertools.combinations(target_chains, 2):
	# reload structures (I know this is ineficient)
	structureA = P.get_structure('A', '%s_%s.pdb' % (pdb_name, chainA_idx))
	structureB = P.get_structure('B', '%s_%s.pdb' % (pdb_name, chainB_idx))
	#
	reslistA = [r for r in structureA[0][chainA_idx].get_residues()]
	reslistB = [r for r in structureB[0][chainB_idx].get_residues()]
	#
	for rA in reslistA:
		# atomlistA = rA.child_dict.values()
		for rB in reslistB:
			# exit()

			dist = min([(a-b) for a in rA.get_atoms() for b in rB.get_atoms()])
			if dist <= dist_threshold:
					# print rA, rB, dist
					resnumA = rA.id[1]
					resnumB = rB.id[1]
					#
					interface_dic[chainA_idx].append(resnumA)
					interface_dic[chainB_idx].append(resnumB)

out = open('%s.list' % pdb_name,'w')
for c in interface_dic:
	int_str = list(set(interface_dic[c]))
	int_str.sort()
	# int_str.sort()
	out.write('%s %s\n' % (c,','.join(map(str, int_str))))
out.close()

out = open('%s.tbl' % pdb_name, 'w')
for e in itertools.permutations(target_chains, 2):
	a, b = e
	for i in list(set(interface_dic[a])):
		tbwA = 'resid %i and segid %s' % (i, a)
		tbwB = []
		for j in list(set(interface_dic[b])):
			tbwB.append('( resid %i and segid %s )' % (j, b))
			# print '( resid %i and segid %s )' % (j, b)
		#
		out.write('assign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
		# exit()
out.close()












