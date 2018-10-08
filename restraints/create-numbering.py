
import sys, os, glob, operator, subprocess, string, argparse
from operator import itemgetter
from itertools import groupby

global haddocktools_path
# haddocktools_path = '/Users/rvhonorato/alc/tools'
#haddocktools_path = '/home/software/haddock/haddock2.3/tools'
haddocktools_path = os.environ['HADDOCKTOOLS']

def run(cmd, outputf):
	with open("./%s" % outputf, "w") as f:
		process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
		process.wait()

def retrieve_seqs(fastaf):
	
	aln_data = open(fastaf).readlines()
	header_idxs = [i for i, e in enumerate(aln_data) if '>' in e] 
	seql = [i for i, e in enumerate(aln_data) if  not '>' in e] 
	seq_idx_list = [range(r[0], r[1]+1) for r in get_range(seql)]

	seq_dic = {}
	for i, idx in enumerate(header_idxs):
		header = aln_data[idx]
		sequence = ''
		for sidx in seq_idx_list[i]:
			sequence += aln_data[sidx]
		
		chain = header.split()[0].split('_')[-1]
		seq_dic[chain] = ''.join(sequence.split())
	return seq_dic
def get_range(data):
	### shamelessly copied from https://stackoverflow.com/a/2154437
	ranges = []
	for k, g in groupby(enumerate(data), lambda (i,x):i-x):
		group = map(itemgetter(1), g)
		ranges.append((group[0], group[-1]))
	return ranges



reference = sys.argv[1]
pdb_dic = {'A':sys.argv[2], 'B':sys.argv[3]}

print pdb_dic 


clustalo_exe = '/home/rodrigo/clustal-omega'

ref_seqf = 'reference.fasta'
cmd = 'python /home/rodrigo/pdb-tools/pdb_toseq.py %s' % reference
run(cmd, ref_seqf)
ref_seq_dic = retrieve_seqs(ref_seqf)


len_dic = {}
for chain in pdb_dic:

	open('ref.fasta','w').write('>ref\n%s\n' % ref_seq_dic[chain])

	pdb = pdb_dic[chain]
	seqf = pdb.replace('.pdb','.fasta')
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

	ref_seq_aln = aln_list[0]
	ubound_seq_aln = aln_list[1]

	# ref_res_l = list(set([int(l.split()[5]) for l in open(reference).readlines() if 'ATOM' in l[:4] and chain == l.split()[4]]))
	ref_res_l = list(set([int(l[22:26]) for l in open(reference).readlines() if 'ATOM' in l[:4] and chain == l[21]]))
	# chain_res_l = list(set([int(l.split()[5]) for l in open(pdb).readlines() if 'ATOM' in l[:4] and chain == l.split()[4]]))
	chain_res_l = list(set([int(l[22:26]) for l in open(pdb).readlines() if 'ATOM' in l[:4] and chain == l[21]]))

	ref_res_dic = dict([(i+1, e) for i, e in enumerate(ref_res_l)])
	chain_res_dic = dict([(i+1, e) for i, e in enumerate(chain_res_l)])

	counterA = 0
	counterB = 0
	offset = 0
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
			print position, aln, counterA, counterB, resnumA, resnumB 
			# exit()
			if resA != resB:
				print 'WARNING: Reference %s %s does not match target %s %s' % (chain, resA, chain, resB)
			else:
				numbering_list.append((resnumA, resnumB))
		
	# write numbering_chain.param
	out = open('%s-numbering.ref' % chain,'w')
	for pair in numbering_list:
		out.write('%i,%i\n' % (pair[0], pair[1]))
	out.close()

