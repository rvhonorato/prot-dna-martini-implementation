#
###
#
# Prepare input for python CG run
#
###
# 1. Fix chains/segid
# 2. Renumber unbound structures according to reference
# 3. Extract true interface from reference (xtal)
# 4. Convert from AA to CG
#   4.1 get aa2cg.tbl (backmapping)
#   4.2 get dna_restraints.def
#   4.3 fix chain/segids for CG structures
###

import os, sys
import sys, os, glob, operator, subprocess
from operator import itemgetter
from itertools import groupby

global haddocktools_path
haddocktools_path = '/Users/rvhonorato/tools'

#================================================================================================#
def fix_chain_segid(pdb_f):
#
	for l in open(pdb_f).readlines():
		if 'ATOM' in l[:4]:
			break
	#
	chain_check = bool(l[21].split())
	try:
		segid_check = bool(l[72:76].split())
	except IndexError:
		segid_check = False
	#
	if segid_check and not chain_check:
		# add chain
		chainf = pdb_f.replace('.pdb','_chain.pdb')
		cmd = '%s/pdb_segid-to-chain %s' % (haddocktools_path, pdb_f)
		run(cmd, chainf)
		os.rename(chainf, pdb_f)
	elif chain_check and not segid_check:
		# add segid
		segidf = pdb_f.replace('.pdb','_segid.pdb')
		cmd = '%s/pdb_chain-to-segid %s' % (haddocktools_path, pdb_f)
		run(cmd, segidf)
		os.rename(segidf, pdb_f)


def run(cmd, outputf):
	with open("./%s" % outputf, "w") as f:
		process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
		process.wait()


def retrieve_seqs(fastaf):
	# print aln
	aln_data = open(fastaf).readlines()
	header_idxs = [i for i, e in enumerate(aln_data) if '>' in e] 
	seql = [i for i, e in enumerate(aln_data) if  not '>' in e] 
	# seq_idx_list = [list(set(e)) for e in get_range(seql)]
	seq_idx_list = [range(r[0], r[1]+1) for r in get_range(seql)]

	seq_dic = {}
	for i, idx in enumerate(header_idxs):
		# print i, idx
		header = aln_data[idx]
		sequence = ''
		for sidx in seq_idx_list[i]:
			sequence += aln_data[sidx]
		#
		chain = header.split()[0].split('_')[-1]
		seq_dic[chain] = ''.join(sequence.split())
		# print header, sequence
	return seq_dic

def get_range(data):
	### shamelessly copied from https://stackoverflow.com/a/2154437
	ranges = []
	for k, g in groupby(enumerate(data), lambda (i,x):i-x):
		group = map(itemgetter(1), g)
		ranges.append((group[0], group[-1]))
	return ranges

#================================================================================================#
#
# prepare_input.py <reference_complex> <unbound1> <unbound2> (<unbound3>)
#
#================================================================================================#
# 0. Input
#
# NOTE: CHAIN SEQUENCE MUST MATCH REFERENCE
#   If reference has (A, C, B)
# $ prepare_input.py <reference> protein1(A) dna(C) protein2(B)
#   If reference has (A, B, C)
# $ prepare_input.py <reference> protein1(A) protein2(B) dna(C)
#
# This could be improved by structuctural superposition and automatic detection
#
#================================================================================================#
reference = sys.argv[1]
reference_cg = reference.replace('.pdb', '_cg.pdb')

# how many chains?
chain_list = list(set([l[21] for l in open(reference).readlines() if 'ATOM' in l [:4]]))
chain_list.sort()

# unbound input must be the same as the number of chains
if len(sys.argv[2:-1]) != len(chain_list):
	print 'ERROR: reference has %i chains, %i inputted pdbs' % (len(chain_list), len(sys.argv[2:]))
	exit()

elif len(sys.argv[2:-1]) == len(chain_list):
	pdb_dic = {}
	for i, pdb in enumerate(sys.argv[2:-1]):
		pdb_dic[chain_list[i]] = pdb
		print '> %s:%s' % (chain_list[i], pdb)

# exit()

dna_chain = sys.argv[-1]

#================================================================================================#
# 1. fix chain/segid
#================================================================================================#
fix_chain_segid(reference)

for chain in pdb_dic:
	pdb = pdb_dic[chain]
	fix_chain_segid(pdb)

#================================================================================================#
# 2. Renumber unbound structures according to reference and get numbering reference file
#================================================================================================#
clustalo_exe = '/Users/rvhonorato/software/clustal-omega-1.2.3-macosx'

ref_seqf = 'reference.fasta'
cmd = 'python /Users/rvhonorato/pdb-tools/pdb_toseq.py %s' % reference
run(cmd, ref_seqf)
ref_seq_dic = retrieve_seqs(ref_seqf)

len_dic = {}

# exit()
for chain in pdb_dic:

	open('ref.fasta','w').write('>ref\n%s\n' % ref_seq_dic[chain])

	pdb = pdb_dic[chain]
	seqf = pdb.replace('.pdb','.fasta')
	cmd = 'python /Users/rvhonorato/pdb-tools/pdb_toseq.py %s' % pdb
	run(cmd, seqf)

	# prepare alignment
	aln_outf = '%s.aln' % chain
	os.system('cat ref.fasta %s > seqs.fasta' % seqf)
	cmd = '%s -i seqs.fasta --outfmt=clu --resno --wrap=9000 --force' % clustalo_exe
	run(cmd, aln_outf)

	aln_list = []
	# identity 
	for l in open(aln_outf):
		if 'ref' in l:
			aln_list.append(l.split()[1])
		elif pdb.split('.')[0] in l:
			aln_list.append(l.split()[1])

	ref_seq_aln = aln_list[0]
	ubound_seq_aln = aln_list[1]

	# print 

	seqA_counter = 0;seqB_counter = 0;offset=0
	numbering_list = []
	for i, aln in enumerate(zip(ref_seq_aln, ubound_seq_aln)):
		#
		resA = aln[0]
		resB = aln[1]
		#
		if resA != '-':
			seqA_counter += 1
		if resB != '-':
			seqB_counter += 1
		#
		if not '-' in aln:
			if resA != resB:
				print 'WARNING: Reference chain %s aa %s position %i does not match target chain %s aa %s' % (chain, resA, i, chain, resB)
			else:
				# print seqA_counter, resA, seqB_counter, resB
				numbering_list.append((seqA_counter, seqB_counter))
		

	# # check for repeated pairs
	# A = [e[0] for e in numbering_list]
	# B = [e[1] for e in numbering_list]
	# blacklist = []
	# for pair in numbering_list:
	#   if A.count(pair[0]) > 1 or B.count(pair[1]) > 1:
	#       blacklist.append(pair)
	#   elif pair[0] == 0 or pair[1] == 0:
	#       blacklist.append(pair)
	#
	# for pair in blacklist:
	#   numbering_list.remove(pair)

	# write numbering_chain.param
	out = open('%s-numbering.ref' % chain,'w')
	for pair in numbering_list:
		out.write('%i,%i\n' % (pair[0], pair[1]))
	out.close()


#================================================================================================#
# 3. Extract true interface from reference (xtal)
#================================================================================================#

# # get accessibilities
# # exit()
# cmd = 'naccess %s' % reference
# run(cmd, 'nacess.log')

# rsaf = reference.replace('.pdb','.rsa')

# accessibilites_blacklist = []
# for l in open(rsaf):
# 	if 'RES' in l[:3]:
# 		data = l.split()
# 		resname = data[1]
# 		chain = data[2]
# 		resnum = int(data[3])
# 		# #
# 		# aa_abs = data[4]
# 		# aa_res = data[5]
# 		#
# 		tot_side_abs = data[6]
# 		tot_side_rel = float(data[7])
# 		#
# 		# bb_abs = data[8]
# 		bb_rel = float(data[9])
# 		# #
# 		# np_abs = data[10]
# 		# np_res = data[11]
# 		# #
# 		# p_abs = data[12]
# 		# p_rel = data[13]
# 		#
# 		if tot_side_rel <= 30.0 or bb_rel <= 30.0:
# 			# print resname, chain, resnum, tot_side_rel, bb_rel
# 			if chain != dna_chain:
# 				print l
# 				accessibilites_blacklist.append( (chain, resnum) )
# 			# print l
# 			# break



distance_threshold = 4.0
contact_outf = 'ref_%i.contacts' % distance_threshold
cmd = '%s/contact %s %i' % (haddocktools_path, reference, distance_threshold)
run(cmd, contact_outf)

# crate a dictionary and populate with 

unpaired_interface_res_dic = dict([(c, []) for c in chain_list])
# active_sidechain_dic = dict([(c, {}) for c in chain_list])

bb_atoms = ['CA','C','O','N','P','O1P','O2P','O5\'','OP1','OP2','C5\'','O4\'','C4\'','C3\'','C2\'','C1\'']

# categorize contacts...!
# bb-bb, bb-sc, sc-sc
# atag = ''
# btag = ''
# t_dic = dict([(c, []) for c in chain_list])
# contact_type_dic = {'bb-bb': t_dic, 
	# 'bb-sc': t_dic, 
	# 'sc-sc': t_dic}

# contact_type_dic = {'bb-bb':{}, 'bb-sc':{}, 'sc-sc':{}}
contact_type_dic = {}
for l in open(contact_outf):
	#
	resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
	#
	resA = int(resA)
	resB = int(resB)
	#
	# check if this contact is bb-bb or bb-sc or sc-sc
	# which atoms are involved?
	###
	if atomA in bb_atoms:
		atype = 'bb'
	else:
		atype = 'sc'
	###
	if atomB in bb_atoms:
		btype = 'bb'
	else:
		btype = 'sc'
	###
	#
	try:
		contact_type_dic[ (chainA, resA) ].append(atype)
	except:
		contact_type_dic[ (chainA, resA) ] = []
		contact_type_dic[ (chainA, resA) ].append(atype)
	#
	try:
		contact_type_dic[ (chainB, resB) ].append(btype)
	except:
		contact_type_dic[ (chainB, resB) ] = []
		contact_type_dic[ (chainB, resB) ].append(btype)
	

# for contact in contact_type_dic:
# 	print contact, list(set(contact_type_dic[contact]))
# 	chain = contact[0]
# 	if len(set(contact_type_dic[contact])) == 1:
# 		t = list(set(contact_type_dic[contact]))[0]
# 		if t == 'sc-sc':
# 			# if chain == dna_chain:
# 			print '*'*10, '(name SC*)'
# 		if t == 'bb-bb':
# 			print '*'*10, '(name BB*)'
# 	# print '-'*42



interface_res_dic = dict([(c, {}) for c in chain_list])
for l in open(contact_outf):
	#
	resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
	###
	#
	resA = int(resA)
	resB = int(resB)
	#
	#
	# if (chainA, resA) in accessibilites_blacklist or (chainB, resB) in accessibilites_blacklist:
	# 	continue
	#
	# if (chainA == dna_chain and chainB != dna_chain) or (chainB == dna_chain and chainA != dna_chain):
	# first set
	try:
		interface_res_dic[chainA][resA].append(chainB)
	except:
		interface_res_dic[chainA][resA] = []
		interface_res_dic[chainA][resA].append(chainB)
	# second set
	try:
		interface_res_dic[chainB][resB].append(chainA)
	except:
		interface_res_dic[chainB][resB] = []
		interface_res_dic[chainB][resB].append(chainA)
	# unpaired
	unpaired_interface_res_dic[chainA].append(resA)
	unpaired_interface_res_dic[chainB].append(resB)


out = open('ambig-autom.tbl','w')
# out_aa = open('ambig-aa.tbl','w')

for chainA in interface_res_dic:
	# print interface_res_dic[chainA]
	numbering_refA =  dict([map(int, a.split(',')) for a in open('%s-numbering.ref' % chainA)])
	#
	for bound_resA in interface_res_dic[chainA].keys():
		try:
			unbound_resA = numbering_refA[bound_resA]
			# unbound_resA_l.append(unbound_resA)
		except KeyError:
			print 'WARNING: Reference Res %i not found in unbound chain %s' % (bound_resA, chain)
			continue
		#
		contact_type_l = list(set(contact_type_dic[ (chainA, bound_resA) ]))
		if len(contact_type_l) == 1:
			contact_t_A = contact_type_l[0]
			if contact_t_A == 'sc':
				tbwAtoms = '(name SC*)'
			elif contact_t_A == 'bb':
				tbwAtoms = '(name BB*)'
			else: # sc-bb
				tbwAtoms = None
			#
			if tbwAtoms:
				tbwA = 'resid %i and segid %s and %s' % (unbound_resA, chainA, tbwAtoms)
				tbwB = []
				for chainB in list(set(interface_res_dic[chainA][bound_resA])):
					#
					numbering_refB =  dict([map(int, a.split(',')) for a in open('%s-numbering.ref' % chainB)])
					#
					active_reslist = interface_res_dic[chainB].keys()
					for bound_resB in active_reslist:
						try:
							unbound_resB = numbering_refB[bound_resB]
							# unbound_resA_l.append(unbound_resA)
						except KeyError:
							print 'WARNING: Reference Res %i not found in unbound chain %s' % (bound_resB, chain)
							exit()
							continue
						#
						for candidate_chain in list(set(interface_res_dic[chainB][bound_resB])):
							if candidate_chain == chainA:
								#
								## which atoms?
								contact_type_l = list(set(contact_type_dic[ (chainB, bound_resB) ]))
								tbwAtoms = None
								if len(contact_type_l) == 1:
									contact_t_B = contact_type_l[0]
									if contact_t_A == contact_t_B:
										if contact_t_B == 'sc':
											tbwAtoms = '(name SC*)'
										elif contact_t_B == 'bb':
											tbwAtoms = '(name BB*)'
									# print contact_t
								# print contact_type_l
								# atom_list = list(set(active_sidechain_dic[chainB][bound_resB]))
								# # print atom_list
								# # exit()
								# if atom_list:
								# 	tbwAtom = ''
								# 	for atom in atom_list:
								# 		tbwAtom += ' name %s or' % atom
								# 	tbwB.append('( resid %i and segid %s and (%s ) )' % (unbound_resB, chainB, tbwAtom[:-2]))
								# else:
								# 	tbwB.append('( resid %i and segid %s )' % (unbound_resB, chainB))
								#
								# tbwB.append('( resid %i and segid %s and (name SC*) )' % (unbound_resB, chainB))
								# print tbwAtoms
								if tbwAtoms:
									tbwB.append('( resid %i and segid %s and %s )' % (unbound_resB, chainB, tbwAtoms))
								# else:
									# tbwB.append('( resid %i and segid %s )' % (unbound_resB, chainB))
						# print resA, chainA, resB, chainB
		# print '\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB))
				if tbwB:
					out.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
		# out_aa.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB_aa)))
out.close()
# out_aa.close()

# exit()

active_res_dic = dict([(chain, map(int, list(set(unpaired_interface_res_dic[chain])))) for chain in unpaired_interface_res_dic])
unbound_active_res_dic = dict([(c, []) for c in chain_list])
# fix numbering according
for chain in active_res_dic:
#
	numbering_ref =  dict([map(int, a.split(',')) for a in open('%s-numbering.ref' % chain)])
	#
	unbound_res_l = []
	for bound_res in active_res_dic[chain]:
		try:
			unbound_res = numbering_ref[bound_res]
			unbound_res_l.append(unbound_res)
		except KeyError:
			print 'WARNING: Reference Res %i not found in unbound chain %s' % (bound_res, chain)
			continue
	unbound_res_l.sort()
	unbound_active_res_dic[chain] = unbound_res_l

# generate active.list
out = open('active.list','w')
for chain in unbound_active_res_dic:
  # print chain, unbound_active_res_dic[chain]
  out.write('sele %s, chain %s and resid %s\n' % (chain, chain, '+'.join(map(str, unbound_active_res_dic[chain]))))
out.close()

# # crate a dictionary and populate with 
# interface_res_dic = dict([(c, {}) for c in chain_list])
# unpaired_interface_res_dic = dict([(c, []) for c in chain_list])
# for l in open(contactf):
#     resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
#     #
#     resA = int(resA)
#     resB = int(resB)
#     # first set
#     try:
#         interface_res_dic[chainA][resA].append(chainB)
#     except:
#         interface_res_dic[chainA][resA] = []
#         interface_res_dic[chainA][resA].append(chainB)
#     # second set
#     try:
#         interface_res_dic[chainB][resB].append(chainA)
#     except:
#         interface_res_dic[chainB][resB] = []
#         interface_res_dic[chainB][resB].append(chainA)
#     # unpaired
#     unpaired_interface_res_dic[chainA].append(resA)
#     unpaired_interface_res_dic[chainB].append(resB)


# # 1. Define restraints according to the interface pairing
# #  Ex. Chain A has contacts with B, C and F
# #    resid resA segidA ( assign ( active res B) ( active res F) )
# out = open('ambig-paired.tbl','w')
# for chainA in interface_res_dic:
#     # print interface_res_dic[chainA]
#     for resA in interface_res_dic[chainA].keys():
#         tbwA = 'resid %i and segid %s' % (resA, chainA)
#         tbwB = []
#         for chainB in list(set(interface_res_dic[chainA][resA])):
#             active_reslist = interface_res_dic[chainB].keys()
#             for resB in active_reslist:
#                 for candidate_chain in list(set(interface_res_dic[chainB][resB])):
#                     if candidate_chain == chainA:
#                         tbwB.append('( resid %i and segid %s )' % (resB, chainB))
#                         # print resA, chainA, resB, chainB
#         out.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
# out.close()


# #
# distance_threshold = 4.0
# contact_outf = 'ref_%i.contacts' % distance_threshold
# cmd = '%s/contact %s %i' % (haddocktools_path, reference, distance_threshold)
# run(cmd, contact_outf)

# interface_res_dic = dict([(c, []) for c in chain_list])
# for l in open(contact_outf):
#   resA,chainA,atomA,resB,chainB,atomB,dist = l.split()
#   interface_res_dic[chainA].append(resA)
#   interface_res_dic[chainB].append(resB)

# active_res_dic = dict([(chain, map(int, list(set(interface_res_dic[chain])))) for chain in interface_res_dic])

# unbound_active_res_dic = dict([(c, []) for c in chain_list])
# # fix numbering according
# for chain in active_res_dic:

#   numbering_ref =  dict([map(int, a.split(',')) for a in open('%s-numbering.ref' % chain)])
#   #
#   unbound_res_l = []
#   for bound_res in active_res_dic[chain]:
#       try:
#           unbound_res = numbering_ref[bound_res]
#           unbound_res_l.append(unbound_res)
#       except KeyError:
#           print 'WARNING: Reference Res %i not found in unbound chain %s' % (bound_res, chain)
#           continue
#   unbound_res_l.sort()
#   unbound_active_res_dic[chain] = unbound_res_l

# # generate active.list
# out = open('active.list','w')
# for chain in unbound_active_res_dic:
#   # print chain, unbound_active_res_dic[chain]
#   out.write('sele %s, chain %s and resid %s\n' % (chain, chain, '+'.join(map(str, unbound_active_res_dic[chain]))))
# out.close()

# # generate ambig.tbl
# out = open('ambig.tbl','w')
# for a in chain_list:
#   for rA in list(set(unbound_active_res_dic[a])):
#       tbwA = 'resid %i and segid %s' % (rA, a)
#       tbwB = []
#       for b in chain_list:
#           if b != a:
#               for rB in list(set(unbound_active_res_dic[b])):
#                   tbwB.append('( resid %i and segid %s )' % (rB, b))
#       out.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
# out.close()


#================================================================================================#
# 4. Convert from AA to CG
#================================================================================================#
aa2cgf = 'cg2aa.tbl'
if os.path.isfile(aa2cgf):
	os.system('rm %s' % aa2cgf)

sorted_chains = pdb_dic.keys()
sorted_chains.sort()

for chain in sorted_chains: 
	pdbf = pdb_dic[chain]
	cg_outf = pdbf.replace('.pdb','_cg.pdb')
	backmap_outf = pdbf.replace('.pdb','_cg_to_aa.tbl')
	cmd = 'python /Users/rvhonorato/Nostromo/aa2cg/aa2cg-prot_dna.py %s' % pdbf
	run(cmd, 'log')
	#
	#   4.1 get aa2cg.tbl (backmapping)
	os.system('cat %s >> %s' % (backmap_outf, aa2cgf))
	#   4.2 fix segids/chain
	fix_chain_segid(cg_outf)


#   4.3 get dna_restraints.def
if not os.path.isfile('dna_restraints.def'):
	print 'ERROR: dna_restraints.def not generated, is there a DNA molecule? check aa2cg conversion'
	exit()

if not os.path.isfile('dna-aa_groups.dat'):
	print 'ERROR: dna-aa_groups.dat not generated, this is needed for DNA restrictions, check aa2cg conversion'
	exit()


#================================================================================================#
# 5. Prepare the package
#================================================================================================#
os.system('mkdir input')
pymol_tbw = 'from pymol import cmd, stored\n'
# pymol_tbw += 'cmd.load(\'%s\')\n' % reference
pymol_tbw += 'cmd.load(\'%s\')\n' % reference.replace('complex', 'ubcomplex')

for chain in pdb_dic:
	pdbf = pdb_dic[chain]
	pdbcgf = pdbf.replace('.pdb','_cg.pdb')
	#
	os.system('cp %s input/' % pdbf)
	os.system('cp %s input/' % pdbcgf)
	#
	# pymol_tbw += 'cmd.load(\'%s\')\n'%pdbf

os.system('cp dna_restraints.def input/')
os.system('cp dna-aa_groups.dat input/')
os.system('cp cg2aa.tbl input/')
os.system('cp ambig-autom.tbl input/')
# os.system('cp ambig-aa.tbl input/')

# this might be usefull for the analysis
os.system('cp *-numbering.ref input/')

if len(chain_list) == 2:
	cmd = '~/run-cg-2.sh'
if len(chain_list) == 3:
	cmd = '~/run-cg-3.sh'

tbw = ''
for chain in chain_list:
	tbw += ' %s' % pdb_dic[chain]

open('input/prepare-run.sh', 'w').write('%s %s' % (cmd + tbw, dna_chain))

for chain in unbound_active_res_dic:
	pymol_tbw += 'cmd.select(\'%s\', \'chain %s and resid %s\')\n' % (chain, chain, '+'.join(map(str, unbound_active_res_dic[chain])))

open('debug-restraints-pymol.py','w').write(pymol_tbw)

#================================================================================================#
# 6. BONUS ROUND - prepare files for analysis
#================================================================================================#

referencecgf = reference.replace('.pdb','_cg.pdb')
cmd = 'python /Users/rvhonorato/Nostromo/aa2cg/aa2cg-prot_dna.py %s' % reference
run(cmd, 'log')

os.system('cp %s input/' % referencecgf)
os.system('cp %s input/' % reference)

#
print 'DONE - you still need to prepare the ambig.tbl (or rename ambig-autom.tbl)'






