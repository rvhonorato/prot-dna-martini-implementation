# given a list of .pdbs put them in the correct place
import glob, os

ls = glob.glob('*pdb')

for p in ls:
	name = p.split('.pdb')[0]
	if not os.path.isdir(name):
		os.system('mkdir %s' % name)
	os.system('cp %s %s/'% (p, name))
	os.system('cp %s %s/%s.bak'% (p, name,name))
