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


# reference = '1BY4_complex_cg.pdb'
# fix_chain_segid(reference_cg)

# bb_list = ['BB', 'BB1', 'BB2', 'BB3']
# for distance_threshold in range(1,10+1):
# 	contact_outf = 'ref_%i.contacts' % distance_threshold
# 	cmd = '%s/contact %s %i' % (haddocktools_path, reference, distance_threshold)
# 	run(cmd, contact_outf)
# 	c = 0
# 	for l in open(contact_outf):
# 		resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
# 		#
# 		if atomA not in bb_list and atomB not in bb_list:
# 			c += 1
# 			# print l
# 	print distance_threshold, c


distance_threshold = 4.0
contact_outf = 'ref_%i.contacts' % distance_threshold
cmd = '%s/contact %s %i' % (haddocktools_path, reference, distance_threshold)
run(cmd, contact_outf)

# # find out where is the DNA
# moltype = dict([(c, []) for c in chain_list])
# for l in open(contact_outf):
# 	resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
# 	if atomA == 'BB':
# 		moltype[chainA].append('protein')
# 	if atomA in ['BB1', 'BB2','BB3']:
# 		moltype[chainA].append('DNA')
# 	#
# 	if atomB == 'BB':
# 		moltype[chainB].append('protein')
# 	if atomB in ['BB1', 'BB2','BB3']:
# 		moltype[chainB].append('DNA')

# moldic = dict([(c, list(set(moltype[c]))) for c in moltype])

# crate a dictionary and populate with 
interface_res_dic = dict([(c, {}) for c in chain_list])
unpaired_interface_res_dic = dict([(c, []) for c in chain_list])
# active_sidechain_dic = dict([(c, {}) for c in chain_list])
for l in open(contact_outf):
	resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
	#
	resA = int(resA)
	resB = int(resB)
	#
	# molA = moldic[chainA][0]
	# molB = moldic[chainB][0]
	if (chainA == dna_chain and chainB != dna_chain) or (chainB == dna_chain and chainA != dna_chain):
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
		# print l
		# exit() 
	#
	# print l, molA, molB
	#
	## select only protein-dna
	# if (molA == 'protein' and molB == 'DNA') or (molB == 'protein' and molA == 'DNA'):
		## is any DNA sidechain in contact with protein sidechain?
		# if atomA not in bb_list and atomB not in bb_list:
		#
		# try:
		# 	active_sidechain_dic[chainA][resA].append(atomA)
		# except:
		# 	active_sidechain_dic[chainA][resA] = []
		# 	active_sidechain_dic[chainA][resA].append(atomA)
		# #
		# try:
		# 	active_sidechain_dic[chainB][resB].append(atomB)
		# except:
		# 	active_sidechain_dic[chainB][resB] = []
		# 	active_sidechain_dic[chainB][resB].append(atomB)

out = open('ambig.tbl','w')
out_aa = open('ambig-aa.tbl','w')

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
		tbwA = 'resid %i and segid %s' % (unbound_resA, chainA)
		tbwB = []
		tbwB_aa = []
		#
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
					continue
				#
				for candidate_chain in list(set(interface_res_dic[chainB][bound_resB])):
					if candidate_chain == chainA:
						#
						## which atoms?
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
						tbwB.append('( resid %i and segid %s and name SC* )' % (unbound_resB, chainB))
						tbwB_aa.append('( resid %i and segid %s )' % (unbound_resB, chainB))
						# print resA, chainA, resB, chainB
		# print '\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB))
		out.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
		out_aa.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB_aa)))
out.close()
out_aa.close()

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
aa2cgf = 'aa2cg.tbl'
if os.path.isfile(aa2cgf):
	os.system('rm %s' % aa2cgf)

for chain in pdb_dic: 
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
os.system('cp aa2cg.tbl input/')
os.system('cp ambig.tbl input/')
os.system('cp ambig-aa.tbl input/')

# this might be usefull for the analysis
os.system('cp *-numbering.ref input/')

if len(chain_list) == 2:
	cmd = '~/run-cg-2.sh'
if len(chain_list) == 3:
	cmd = '~/run-cg-3.sh'

tbw = ''
for chain in chain_list:
	tbw += ' %s' % pdb_dic[chain]

open('input/prepare-run.sh', 'w').write('%s' % (cmd + tbw))

#

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







