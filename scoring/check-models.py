import glob,os

pdbl = [e for e in glob.glob('*pdb') if not 'conv' in e]

fl = [e for e in glob.glob('filelist*') if e != 'filelist.list' and not 'ori' in e]

for f in fl:
	for pdb in open(f):
		conv = pdb.split('/')[-1][:-2].replace('.pdb','_conv.pdb')
		#conv = pdb.replace('.pdb', '_conv.pdb')
		if not os.path.isfile(conv):
			print f, conv
			break
