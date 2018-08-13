# some models have positive internal energies, this most likely means that they re mashed together, filter them out
import glob

ls = glob.glob('*conv.pdb')

c = 1
for pdb in ls:
	data = open(pdb).readlines()
	internal_e_comp = float(data[23].split()[-1])
	if internal_e_comp > 0:
		print pdb
		c += 1