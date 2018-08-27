import glob,os, commands

qstat = commands.getstatusoutput('qstat -u rodrigo')[1]

running_l = [int(e.split('scoring')[-1][:-4]) for e in qstat.split() if 'scoring' in e]

pdbl = [e for e in glob.glob('*scoring*pdb') if not 'conv' in e]

fl = [e for e in glob.glob('filelist*') if e != 'filelist.list' and not 'ori' in e]

sc_check = dict([(p, commands.getstatusoutput('grep "CG" %s' % p)[0]) for p in pdbl]) 

for f in fl:
	f_idx = int(f.split('filelist')[-1].split('.')[0])
	if f_idx not in running_l:
		pdb_l = [p.split('/')[-1][:-2] for p in open(f).readlines()]
		for i, pdb in enumerate(pdb_l):
			check = sc_check[pdb]
			if check != 0:
				# model has sidechains
				try:
					nextpdb = pdb_l[i+1]
				except:
					continue
				check2 = sc_check[nextpdb]
				if check2 == 0:
					conv = nextpdb.replace('.pdb','_conv.pdb')
					if not os.path.isfile(conv):
						print pdb, 'no SC - breakpoint, remove from', f
						exit()
						break

