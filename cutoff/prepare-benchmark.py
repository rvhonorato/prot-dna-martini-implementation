import os, subprocess, itertools

def run(cmd, outputf):
	with open(outputf, "w") as f:
	    process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
	    process.wait()

target_l = ['1AZS', '1EXB', '1GXD', '1KXP', '1RLB', '1T6B', '1WDW', '2AJF', '2FJU', '2GAF', '2OOR', '3BIW', '3BP8', '3LVK', '4H03']

source_path = '/home/jroel/CG_benchmark/cg'

cutoff_range = [8.5, 10, 12, 14]


prod_l = list(itertools.product(cutoff_range, cutoff_range))

out = open('README','w')
for i, e in enumerate(prod_l):
	out.write('run%i it0 %.1f it1 %.1f\n' % (i, e[0], e[1]))
out.close()


for target in target_l:
	#
	if not os.path.isdir(target):
		os.system('mkdir %s' % target)
	#
	ambig = '%s/%s/run3/data/distances/ambig.tbl' % (source_path, target)
	cg2aa = '%s/%s/run3/data/distances/cg-to-aa.tbl' % (source_path, target)
	#
	pA = '%s/%s/protein1.pdb' % (source_path, target)
	pB = '%s/%s/protein2.pdb' % (source_path, target)
	pA_cg = '%s/%s/protein1_cg.pdb' % (source_path, target)
	pB_cg = '%s/%s/protein2_cg.pdb' % (source_path, target)
	#
	os.system('cp %s %s/' % (ambig, target))
	os.system('cp %s %s/' % (cg2aa, target))
	os.system('cp %s %s/' % (pA, target))
	os.system('cp %s %s/' % (pB, target))
	os.system('cp %s %s/' % (pA_cg, target))
	os.system('cp %s %s/' % (pB_cg, target))

	for i, cutoff in enumerate(prod_l):

		param = '''CGTOAA_TBL=./cg-to-aa.tbl
AMBIG_TBL=./ambig.tbl
HADDOCK_DIR=/home/abonvin/haddock2.4
N_COMP=2
PDB_FILE1=./protein1.pdb
PDB_FILE2=./protein2.pdb
CGPDB_FILE1=./protein1_cg.pdb
CGPDB_FILE2=./protein2_cg.pdb
PROJECT_DIR=./
PROT_SEGID_1=A
PROT_SEGID_2=B
RUN_NUMBER=%i
''' % (i+1)

		open('%s/run.param' % target,'w').write(param)
		open('%s/run.param.%i' % (target, i+1),'w').write(param)

		os.chdir(target)
		cmd = '/usr/bin/python /home/abonvin/haddock_git/haddock2.4/Haddock/RunHaddock.py'
		run(cmd, 'log')
		os.chdir('..')

		os.system('cp /home/rodrigo/Nostromo/cutoff/read_struc.cns %s/run%i/protocols/' % (target, i+1))

		it0_cutoff = cutoff[0]
		it1_cutoff = cutoff[1]

		read_struct_old = open('%s/run%i/protocols/read_struc.cns' % (target, i+1)).readlines()
		                     # '        cutnb=11.0 ctofnb=10.0 ctonnb=8.0 eps=1.0 e14fac=0.4 inhibit 0.25\n'
		read_struct_old[155] = '        cutnb=%.1f ctofnb=%.1f ctonnb=%.1f eps=1.0 e14fac=0.4 inhibit 0.25\n' % (it0_cutoff+1, it0_cutoff, it0_cutoff-2) # it0
		read_struct_old[164] = '        cutnb=%.1f ctofnb=%.1f ctonnb=%.1f eps=1.0 e14fac=0.4 inhibit 0.25\n' % (it1_cutoff+1, it1_cutoff, it1_cutoff-2) # it1

		read_struct_new = open('%s/run%i/protocols/read_struc.cns' % (target, i+1),'w')
		read_struct_new.write(''.join(read_struct_old))
		read_struct_new.close()
		











