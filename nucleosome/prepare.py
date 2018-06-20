#
import os, sys
import sys, os, glob, operator, subprocess
from operator import itemgetter
from itertools import groupby

global haddocktools_path
# haddocktools_path = '/Users/rvhonorato/alc/tools'
haddocktools_path = '/home/software/haddock/haddock2.3/tools'

def fix_chain_segid(pdb_f):

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


whitelist_chains = ['A','B','C','D','E','F','G','H','X']#'I','J'] 


for idx in whitelist_chains:
	target = '4r8p_%s.pdb' % idx
	fix_chain_segid(target)
	cg_outf = target.replace('.pdb','_cg.pdb')
	#
	backmap_outf = target.replace('.pdb','_cg_to_aa.tbl')
	cmd = 'python2.7 /home/rodrigo/Nostromo/aa2cg/aa2cg-prot_dna.py %s' % target
	# cmd = 'python2.7 /Users/rvhonorato/alc/Nostromo/aa2cg/aa2cg-prot_dna.py %s' % pdbf
	print cmd
	run(cmd, 'log')
	# os.system('cat %s >> %s' % (backmap_outf, aa2cgf))
	#   4.2 fix segids/chain
	fix_chain_segid(cg_outf)











# add segids