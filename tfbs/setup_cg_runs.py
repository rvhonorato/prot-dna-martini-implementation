# setup the cg runs
import glob, os, subprocess

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


global haddocktools_path
# haddocktools_path = '/Users/rvhonorato/alc/tools'
haddocktools_path = '/home/software/haddock/haddock2.3/tools'


# setup

# ls = glob.glob('*')

ls = [p.split('.pdb')[0] for p in glob.glob('*pdb') if not 'RARB.pdb' in p]

for target_dna in ls:
	# setup the folder
	f = 'd' + target_dna
	if not os.path.isdir(f):
		os.system('mkdir %s' % f)
		os.system('cp %s.pdb %s' % (target_dna, f))
		os.system('cp RARB.pdb %s' % f)
		os.system('cp ambig.tbl %s' % f)

	os.chdir(f)

	dna_s = target_dna + '.pdb'
	nr_s = 'RARB.pdb'

	# NR
	cmd = 'python /home/rodrigo/pdb-tools/pdb_chain.py -A %s' % nr_s
	run(cmd, 'temp.pdb')
	os.system('cp temp.pdb %s' % nr_s)
	cmd = 'python /home/rodrigo/pdb-tools/pdb_chainxseg.py %s' % nr_s
	run(cmd, 'temp.pdb')
	os.system('mv temp.pdb %s' % nr_s)

	nr_cg_outf = nr_s.replace('.pdb','_cg.pdb')
	nr_backmap_outf = nr_s.replace('.pdb','_cg_to_aa.tbl')
	cmd = 'python2.7 /home/rodrigo/Nostromo/aa2cg/aa2cg-prot_dna_rna.py %s' % nr_s
	print cmd
	run(cmd, 'log')
	fix_chain_segid(nr_cg_outf)

	# DNA
	cmd = 'python /home/rodrigo/pdb-tools/pdb_chain.py -B %s' % dna_s
	run(cmd, 'temp.pdb')
	os.system('cp temp.pdb %s' % dna_s)
	cmd = 'python /home/rodrigo/pdb-tools/pdb_chainxseg.py %s' % dna_s
	run(cmd, 'temp.pdb')
	os.system('mv temp.pdb %s' % dna_s)

	dna_cg_outf = dna_s.replace('.pdb','_cg.pdb')
	dna_backmap_outf = dna_s.replace('.pdb','_cg_to_aa.tbl')
	cmd = 'python2.7 /home/rodrigo/Nostromo/aa2cg/aa2cg-prot_dna_rna.py %s' % dna_s
	print cmd
	run(cmd, 'log')
	fix_chain_segid(dna_cg_outf)

	os.system('cat RARB_cg_to_aa.tbl %s_cg_to_aa.tbl > cg2aa.tbl' % target_dna)

	tbw = '''<html>
<head>
<title>HADDOCK - start</title>
</head>
<body bgcolor=#ffffff>
<h2>Parameters for the start:</h2>
<BR>
<h4><!-- HADDOCK -->
CGTOAA_TBL=./cg2aa.tbl<BR>
AMBIG_TBL=./ambig.tbl<BR>
HADDOCK_DIR=/home/abonvin/haddock2.3/<BR>
N_COMP=2<BR>
PDB_FILE1=./RARB.pdb<BR>
CGPDB_FILE1=./RARB_cg.pdb<BR>
PROT_SEGID_1=A<BR>
PDB_FILE2=./%s.pdb<BR>
CGPDB_FILE2=./%s_cg.pdb<BR>
PROT_SEGID_2=B<BR>
RUN_NUMBER=1<BR>
PROJECT_DIR=./<BR>
submit_save=Save updated parameters<BR>
</h4><!-- HADDOCK -->
</body>
</html>''' % (target_dna, target_dna)
	open('new.html','w').write(tbw)

	open('run.sh','w').write('python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py\nbash /home/rodrigo/Nostromo/scripts/run-cg.sh B')

	os.chdir('..')
