import glob, commands

# pdbl = [e for e in glob.glob('*scoring*pdb') if not 'conv' in e]

pdbl = [e for e in open('filelist.list')]
# fl = [e for e in glob.glob('filelist*') if e != 'filelist.list' and not 'ori' in e]
sc_check = dict([(p.split('"')[1], commands.getstatusoutput('grep "CG" %s' % p.split('"')[1])[0]) for p in pdbl])

blacklist = []
for pdb in sc_check:
	if sc_check[pdb] == 0:
		print '"%s"' %pdb
		# print pdb