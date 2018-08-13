# check which models failed in topology creation
import glob, os

pdbl = [e for e in glob.glob('*pdb') if not 'conv' in e]

for p in pdbl:
	conv = p.replace('.pdb','_conv.pdb')
	if not os.path.isfile(conv):
		print p
