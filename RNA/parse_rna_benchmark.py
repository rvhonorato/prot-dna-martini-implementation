# parse data from the protein-rna benchmark
import glob, os

loc = '/data/benchmark/protein-RNA/bound-bound'
ls = [f for f in glob.glob('%s/*' % loc) if not '.' in f]

tag = 'act-pass-nodesol'

for f in ls:
	pdb_name = f.split('/')[-1]
	#
	struct_list = glob.glob('%s/%s-%s/data/sequence/*pdb' % (f,tag, pdb_name))
	ambig_f = '%s/%s-%s/data/distances/ambig.tbl' % (f, tag, pdb_name)
	unambig_f = '%s/%s-%s/data/distances/unambig.tbl' % (f, tag, pdb_name)
	refe = glob.glob('%s/*refe.pdb' % f)[0]
	# print struct_list, ambig_f, unambig_f, refe
	# also take the restraints...?
	if not os.path.isdir(pdb_name):
		os.system('mkdir %s' % pdb_name)
	for s in struct_list:
		os.system('cp %s %s/' % (s, pdb_name))
	#
	os.system('cp %s %s/%s_complex.pdb' % (refe, pdb_name, pdb_name))
	os.system('cp %s %s/' % (ambig_f, pdb_name))
	os.system('cp %s %s/' % (unambig_f, pdb_name))
	#

	
