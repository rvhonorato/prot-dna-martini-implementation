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
# haddocktools_path = '/Users/rvhonorato/alc/tools'
haddocktools_path = '/home/software/haddock/haddock2.3/tools'

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
		# cmd = 'python /Users/rvhonorato/alc/pdb-tools/pdb_segxchain.py %s' % pdb_f
		run(cmd, chainf)
		os.rename(chainf, pdb_f)
	elif chain_check and not segid_check:
		# add segid
		segidf = pdb_f.replace('.pdb','_segid.pdb')
		cmd = '%s/pdb_chain-to-segid %s' % (haddocktools_path, pdb_f)
		# cmd = 'python /Users/rvhonorato/alc/pdb-tools/pdb_chainxseg.py %s' % pdb_f
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
# prepare_input.py <reference_complex> <unbound1> <unbound2> (<unbound3>) <dna chain>
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

# find what to do
reference = glob.glob('*_complex.pdb')[0]
reference_cg = reference.replace('.pdb', '_cg.pdb')

#
chain_list = list(set([l[21] for l in open(reference).readlines() if 'ATOM' in l [:4]]))

for l in open(reference).readlines():
	if 'ATOM' in l[:4]:
		if l.split()[3] in ['CYT', 'DC', 'THY', 'DT', 'ADE', 'DA', 'GUA', 'DG']:
			dna_chain = l.split()[4]
			break

unbound_l = [p for p in glob.glob('*unbound*pdb') if not 'cg' in p]

# remove redundancies
unbound_dic = dict([(p.split('prot')[-1:][0][:1], []) for p in unbound_l if 'prot' in p])
unbound_dic[dna_chain] = []
for p in unbound_l:
	if not 'prot' in p:
		unbound_dic[dna_chain] = [p]
	else:
		idx = p.split('prot')[-1:][0][:1]
		unbound_dic[idx].append(p)

pdb_dic = {}
for k in unbound_dic:
	t_l = unbound_dic[k]
	t_l.sort()
	pdb_dic[k] = t_l[0]


#================================================================================================#
# 1. fix chain/segid
#================================================================================================#
print '1. fix chain/segid'
fix_chain_segid(reference)

for chain in pdb_dic:
	pdb = pdb_dic[chain]
	fix_chain_segid(pdb)

#================================================================================================#
# 2. Renumber unbound structures according to reference and get numbering reference file
#================================================================================================#
print '2. Renumber unbound structures according to reference and get numbering reference file'
# clustalo_exe = '/Users/rvhonorato/software/clustal-omega-1.2.3-macosx'
# clustalo_exe = '/Users/rvhonorato/clustal-omega-1.2.3-macosx'
clustalo_exe = '/home/rodrigo/clustal-omega'

ref_seqf = 'reference.fasta'
# cmd = 'python /Users/rvhonorato/alc/pdb-tools/pdb_toseq.py %s' % reference
cmd = 'python /home/rodrigo/pdb-tools/pdb_toseq.py %s' % reference
run(cmd, ref_seqf)
ref_seq_dic = retrieve_seqs(ref_seqf)


def valid_atoms(pdb):
	ref_valid_dic = {}
	for l in open(pdb):
		if 'ATOM' in l[:4]:
			atom_name = l.split()[2]
			chain = l.split()[4]
			chain = l[21]
			atom_name = l[12:16]
			resnum = int(l[22:26])
			# print l
			# print l[12:16], l[21], l[22:26]
			# resnum = int(l.split()[5])
			#
			if 'CA' in atom_name or 'P' in atom_name:
				try:
					_ = ref_valid_dic[chain]
				except:
					ref_valid_dic[chain] = []
				#
				ref_valid_dic[chain].append(resnum)
	return ref_valid_dic

# COLUMNS        DATA  TYPE    FIELD        DEFINITION
# -------------------------------------------------------------------------------------
#  1 -  6        Record name   "ATOM  "
#  7 - 11        Integer       serial       Atom  serial number.
# 13 - 16        Atom          name         Atom name.
# 17             Character     altLoc       Alternate location indicator.
# 18 - 20        Residue name  resName      Residue name.
# 22             Character     chainID      Chain identifier.
# 23 - 26        Integer       resSeq       Residue sequence number.
# 27             AChar         iCode        Code for insertion of residues.
# 31 - 38        Real(8.3)     x            Orthogonal coordinates for X in Angstroms.
# 39 - 46        Real(8.3)     y            Orthogonal coordinates for Y in Angstroms.
# 47 - 54        Real(8.3)     z            Orthogonal coordinates for Z in Angstroms.
# 55 - 60        Real(6.2)     occupancy    Occupancy.
# 61 - 66        Real(6.2)     tempFactor   Temperature  factor.
# 77 - 78        LString(2)    element      Element symbol, right-justified.
# 79 - 80        LString(2)    charge       Charge  on the atom.


ref_valid_atoms = valid_atoms(reference)

len_dic = {}
for chain in pdb_dic:

	open('ref.fasta','w').write('>ref\n%s\n' % ref_seq_dic[chain])

	pdb = pdb_dic[chain]
	seqf = pdb.replace('.pdb','.fasta')
	# cmd = 'python /Users/rvhonorato/alc/pdb-tools/pdb_toseq.py %s' % pdb
	cmd = 'python /home/rodrigo/pdb-tools/pdb_toseq.py %s' % pdb
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

	chain_valid_atoms = valid_atoms(pdb)

	ref_seq_aln = aln_list[0]
	ubound_seq_aln = aln_list[1]

	ref_res_l = list(set([int(l.split()[5]) for l in open(reference).readlines() if 'ATOM' in l[:4] and chain == l.split()[4]]))
	chain_res_l = list(set([int(l.split()[5]) for l in open(pdb).readlines() if 'ATOM' in l[:4] and chain == l.split()[4]]))

	ref_res_dic = dict([(i+1, e) for i, e in enumerate(ref_res_l)])
	chain_res_dic = dict([(i+1, e) for i, e in enumerate(chain_res_l)])

	counterA = 0
	counterB = 0
	offset=0
	numbering_list = []
	for position, aln in enumerate(zip(ref_seq_aln, ubound_seq_aln)):
		#
		resA = aln[0]
		resB = aln[1]
		#
		if resA != '-':
			counterA +=1
		if resB != '-':
			counterB +=1
		#
		if not '-' in aln:
			resnumA = ref_res_dic[counterA]
			resnumB = chain_res_dic[counterB]
			# print position, aln, counterA, counterB, resnumA, resnumB 
			# exit()
			if resA != resB:
				print 'WARNING: Reference chain %s aa %s position %i does not match target chain %s aa %s' % (chain, resA, i, chain, resB)
			else:
				# check if this residue is valid
				if resnumA in ref_valid_atoms[chain] and resnumB in chain_valid_atoms[chain]:
					numbering_list.append((resnumA, resnumB))
		
	# write numbering_chain.param
	out = open('%s-numbering.ref' % chain,'w')
	for pair in numbering_list:
		out.write('%i,%i\n' % (pair[0], pair[1]))
	out.close()

#================================================================================================#
# 3. Convert Benchmark AIR to CG
#================================================================================================#
print '3. Convert Benchmark AIR to CG'

bb_d ={"BB1": ["P", "O1P", "O2P", "O5'", "OP1", "OP2"],
"BB2": ["C5'", "O4'", "C4'"],
"BB3": ["C3'", "C2'", "C1'"]}

sc_d = {"SC1": ["N9", "C4", "N1", "C6"],
"SC2": ["O2", "C2", "N2", "N3"],
"SC3": ['C7','N6','O6', 'N1','O4','N4','C6','C5','C4'],
"SC4": ["C8", "N7", "C5"]}

f = 'air_trueiface_unbound.tbl'
if os.path.isfile(f):
	out = open('air_trueiface_unbound-cg.tbl','w')
	for l in open(f).readlines():
		atoms = ''.join(''.join(l.split('name')[1:]).split('))')[0].split('or')).split()
		bb = list(set([b for b in bb_d for e in atoms for c in bb_d[b] if e == c]))
		bb.sort()
		sc = list(set([s for s in sc_d for e in atoms for c in sc_d[s] if e == c]))
		sc.sort()
		if sc:
			n_l = l.split('name')[0] + 'name ' + ' or name '.join(sc) + '))\n'
		elif bb:
			n_l = l.split('name')[0] + 'name ' + ' or name '.join(bb) + '))\n'
		else:
			n_l = l
		#
		out.write(n_l)
	out.close()
else:
	print f, 'not found'
	exit()

#================================================================================================#
# 4. Convert from AA to CG
#================================================================================================#
print '4. Convert from AA to CG'

aa2cgf = 'cg2aa.tbl'
if os.path.isfile(aa2cgf):
	os.system('rm %s' % aa2cgf)

sorted_chains = pdb_dic.keys()
sorted_chains.sort()

for chain in sorted_chains: 
	pdbf = pdb_dic[chain]
	cg_outf = pdbf.replace('.pdb','_cg.pdb')
	backmap_outf = pdbf.replace('.pdb','_cg_to_aa.tbl')
	cmd = 'python2.7 /home/rodrigo/Nostromo/aa2cg/aa2cg-prot_dna.py %s' % pdbf
	# cmd = 'python2.7 /Users/rvhonorato/alc/Nostromo/aa2cg/aa2cg-prot_dna.py %s' % pdbf
	print cmd
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
# 5. Prepare files for analysis
#================================================================================================#
print '5. Prepare files for analysis'

referencecgf = reference.replace('.pdb','_cg.pdb')
# cmd = 'python /Users/rvhonorato/Nostromo/aa2cg/aa2cg-prot_dna.py %s' % reference
cmd = 'python2.7 /home/rodrigo/Nostromo/aa2cg/aa2cg-prot_dna.py %s' % reference
run(cmd, 'log')

# os.system('cp %s input/' % referencecgf)
# os.system('cp %s input/' % reference)

#================================================================================================#
# 6. Run setup
#================================================================================================#
print '6. Run setup'

# write new.html
tbw = '''<html>
<head>
<title>HADDOCK - start</title>
</head>
<body bgcolor=#ffffff>
<h2>Parameters for the start:</h2>
<BR>
<h4><!-- HADDOCK -->
CGTOAA_TBL=./cg2aa.tbl<BR>
AMBIG_TBL=./air_trueiface_unbound-cg.tbl<BR>
HADDOCK_DIR=/home/abonvin/haddock2.3/<BR>
N_COMP=%i<BR>
''' % len(pdb_dic)
chain_list.sort()
for i, chain in enumerate(chain_list):
	print i, chain, pdb_dic[chain]
	cg_f = pdb_dic[chain].replace('.pdb','_cg.pdb')
	tbw += 'PDB_FILE%i=./%s<BR>\n' % (i+1, pdb_dic[chain])
	tbw += 'CGPDB_FILE%i=./%s<BR>\n' % (i+1, cg_f)
	tbw += 'PROT_SEGID_%i=%s<BR>\n' % (i+1, chain)

tbw += '''RUN_NUMBER=1<BR>
PROJECT_DIR=./<BR>
submit_save=Save updated parameters<BR>
</h4><!-- HADDOCK -->
</body>
</html>'''
open('new.html','w').write(tbw)


# run haddock2.3 on cluster

open('run.sh','w').write('python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py\nbash /home/rodrigo/Nostromo/scripts/run-cg.sh %s' % dna_chain)

# cmd = 'haddock2.3'

# HADDOCK="/home/software/haddock/haddock2.3"                                                                                                                                
#HADDOCK="/home/abonvin/haddock2.3-nmol"                                                                                                                                   
# HADDOCKTOOLS="$HADDOCK/tools"                                                                                                                                              
# PYTHONPATH="${PYTHONPATH}:$HADDOCK"                                                                                                                                        
# alias haddock2.3="$(which python) $HADDOCK/Haddock/RunHaddock.py"
# cmd = 'python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py'
# run(cmd, 'out')

# cmd = 'bash /home/rodrigo/Nostromo/scripts/run-cg.sh %s' % dna_chain
# run(cmd, 'out2')