# prepare DNA for aa2cg conversion
## find out if base pairs belong to a double strand or not

# simply check each dna base if its close enought to another one and rename it to hDA, hDG, hDT or hCG
import itertools
from Bio.PDB import PDBParser


def determine_hbonds(structure):
	nuc = ['DA', 'DC', 'DG', 'DT']
	hb_nuc = ['hDA', 'hDC', 'hDG', 'hDT']
	aa = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS", "LEU", "MET", "ASN", "PRO", "GLN", "ARG", "SER", "THR", "VAL", "TRP", "TYR"]
	pairing = {'A':'T', 'C':'G', 'T':'A', 'G':'C'}
	#
	# for model in structure:
	model = structure[0]
	#
	dna_chain_l = []
	for chain in model:
		# print chain
		prot_comp = len([r for r in chain.get_residues() if r.resname.split()[0] in aa])
		dna_comp =  len([r for r in chain.get_residues() if r.resname.split()[0] in nuc])
		hbond_dna_comp = len([r for r in chain.get_residues() if r.resname.split()[0] in hb_nuc])
		#
		if prot_comp:
			print chain, 'is protein'
		if dna_comp:
			print chain, 'is nucleic'
			dna_chain_l.append(chain)
		if hbond_dna_comp:
			print chain, 'is hbond nucleic'
		if dna_comp and prot_comp:
			print chain, 'is mixed'
			exit()
	#
	# check distances!
	## list sizes could be different, this might be improvable
	distance_cutoff = 3.
	for chainA, chainB in itertools.combinations(dna_chain_l, 2):
		#
		reslistA = [r for r in chainA.get_residues()]
		reslistB = [r for r in chainB.get_residues()]
		#
		for rA in reslistA:
			#
			atomlistA = rA.child_dict.values()
			#
			for rB in reslistB:
				#
				atomlistB = rB.child_dict.values()
				#
				baseA = rA.resname.split()[0][-1]
				baseB = rB.resname.split()[0][-1]
				#
				# do all calculations so we can check if there's an incorrect pairing
				distance_list = [a-b for a in atomlistA for b in atomlistB]
				if min(distance_list) <= distance_cutoff:
					#
					if not 'h' in rA.resname:
						rA.resname = 'h' + rA.resname.split()[0]
					if not 'h' in rB.resname:
						rB.resname = 'h' + rB.resname.split()[0]
					#
					if pairing[baseA] != baseB:
						print 'warning, incorrect pairing!'
						exit()
	return structure 



P = PDBParser()
structure = P.get_structure('aa_model', '1dsz_clean.pdb')

s = determine_hbonds(structure)

