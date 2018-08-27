import glob, os, subprocess

def run(cmd, outputf):
	with open(outputf, "w") as f:
	    process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
	    process.wait()

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
		run(cmd, chainf)
		os.rename(chainf, pdb_f)

	elif chain_check and not segid_check:
		# add segid
		segidf = pdb_f.replace('.pdb','_segid.pdb')
		cmd = '%s/pdb_chain-to-segid %s' % (haddocktools_path, pdb_f)
		run(cmd, segidf)
		os.rename(segidf, pdb_f)

global haddocktools_path
# haddocktools_path = '/Users/rvhonorato/alc/tools'
haddocktools_path = '/home/software/haddock/haddock2.3/tools'



paramf_loc = '/data/benchmark/protein-peptide/haddockparam-files-unbound'

for p in glob.glob('%s/*web' % paramf_loc):
	pdb_name = p.split('/')[-1].split('-')[0]
	param_name = p.split('/')[-1]

	print pdb_name
	if not os.path.isdir(pdb_name):
		os.system('mkdir %s' % pdb_name)

	os.chdir(pdb_name)
	os.system('cp %s .' % p)
	cmd = 'perl /home/rodrigo/haddock-CSB-tools/paramFL_related/extractPDBfl_fromHaddockparam.pl %s' % param_name
	run(cmd, 'log')
	pdb_l = ['pdbFL1.pdb','pdbFL2.pdb']

	cmd = os.system('grep -v "HOH" pdbFL1.pdb > oo')
	# run(cmd, 'oo')
	os.system('mv oo pdbFL1.pdb')
	os.system("echo 'END' &>> pdbFL1.pdb")

	# cmd = 'grep -v "HOH" pdbFL2.pdb'
	cmd = os.system('grep -v "HOH" pdbFL2.pdb > oo')
	# run(cmd, 'oo')
	os.system('mv oo pdbFL2.pdb')
	
	cmd = '%s/pdb_setchain -v CHAIN=B pdbFL2.pdb' % haddocktools_path
	run(cmd, 'oo')
	os.system('mv oo pdbFL2.pdb')


	# is this multimodel?
	multicheck = False
	for l in open('pdbFL2.pdb'):
		if 'MODEL' in l:
			multicheck = True

	if multicheck:
		cmd = 'python /home/rodrigo/pdb-tools/pdb_splitmodel.py pdbFL2.pdb'
		run(cmd, 'log')
	else:
		exit()

	# pdb_l = glob.glob('*.pdb')

	tbl_d = {'active': None, 'passive': None}
	for l in open(param_name):
		if 'activereslist' in l:
			active = l.split()[2].split()[0].split("'")[1]
			if len(active) > 0:
				tbl_d['active'] = map(int, active.split(','))
			# print active
			# exit()
		if 'passivereslist' in l:
			passive = l.split()[2].split()[0].split("'")[1]
			if len(passive) > 0:
				tbl_d['passive'] = map(int, passive.split(','))
	
	# gen ambig.tbl
	out = open('ambig.tbl','w')
	for e in tbl_d['active']:
		tbw = 'assign ( resid %i and segid A ) ( \n' % e
		tbw += ' or \n'.join(['( resid %i and segid B )' % i for i in tbl_d['passive']]) + ') 2.0 2.0 0.0\n'
		out.write(tbw+'\n')

	# aa2cg
	pdb_l = [e for e in glob.glob('pdbFL*.pdb') if not 'cg' in e]

	aa2cgf = 'cg2aa.tbl'
	if os.path.isfile(aa2cgf):
		os.system('rm %s' % aa2cgf)

	for pdbf in pdb_l: 
		fix_chain_segid(pdbf)
		cg_outf = pdbf.replace('.pdb','_cg.pdb')
		backmap_outf = pdbf.replace('.pdb','_cg_to_aa.tbl')
		cmd = 'python2.7 /home/rodrigo/Nostromo/aa2cg/aa2cg-prot_dna_rna.py %s' % pdbf
		print cmd
		run(cmd, 'log')
		# 4.1 get aa2cg.tbl (backmapping)
		os.system('cat %s >> %s' % (backmap_outf, aa2cgf))
		#   4.2 fix segids/chain
		fix_chain_segid(cg_outf)

	if multicheck:
		outA = open('fileB.list','w')
		outB= open('fileB-cg.list','w')
		for p in glob.glob('pdbFL2_*_*.pdb'):
				outB.write(p+'\n')
				outA.write(p.split('_cg')[0]+'.pdb\n')


	# new.html
	# write new.html
	tbw = '<html>\n'
	tbw += '<head>\n'
	tbw += '<title>HADDOCK - start</title>\n'
	tbw += '</head>\n'
	tbw += '<body bgcolor=#ffffff>\n'
	tbw += '<h2>Parameters for the start:</h2>\n'
	tbw += '<BR>\n'
	tbw += '<h4><!-- HADDOCK -->\n'
	tbw += 'CGTOAA_TBL=./cg2aa.tbl<BR>\n'
	tbw +='AMBIG_TBL=./ambig.tbl<BR>\n'
	tbw += 'HADDOCK_DIR=/home/abonvin/haddock2.3/<BR>\n'
	tbw += 'N_COMP=2<BR>\n'
	tbw += 'PDB_FILE1=./pdbFL1.pdb<BR>\n'
	tbw += 'CGPDB_FILE1=./pdbFL1_cg.pdb<BR>\n'
	
	tbw += 'PDB_FILE2=./pdbFL2_1.pdb<BR>\n'
	tbw += 'CGPDB_FILE1=./pdbFL2_1_cg.pdb<BR>\n'

	tbw += 'PDB_LIST2=./fileB.list<BR>\n'
	tbw += 'CGPDB_LIST2=./fileB-cg.list<BR>\n'

	tbw += 'PROT_SEGID_1=A<BR>\n'
	tbw += 'PROT_SEGID_2=B<BR>\n'
	tbw += 'RUN_NUMBER=1<BR>\n'
	tbw += 'PROJECT_DIR=./<BR>\n'
	tbw += 'submit_save=Save updated parameters<BR>\n'
	tbw += '</h4><!-- HADDOCK -->\n'
	tbw += '</body>\n'
	tbw += '</html>\n'

	open('new.html','w').write(tbw)
	os.chdir('../')
