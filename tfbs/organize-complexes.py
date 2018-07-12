# given a list of .pdbs put them in the correct place
import glob, os

ls = glob.glob('*pdb')

for p in ls:
	name = p.split('_')[-1].split('.pdb')[0]
	if not os.path.isdir(name):
		os.system('mkdir %s' % name)
	os.system('mv %s %s/%s.pdb'% (p, name, name))
	# os.system('cp %s %s/%s.bak'% (p, name, name))
