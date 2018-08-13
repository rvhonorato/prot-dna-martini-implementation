import glob

# lys_l = [384,385,1235,526,1040,410,231,1184,545,
# 	1188,549,881,168,937,941,1198,1267,1127,959,
# 	966,1225,1227,98,339,854,343,348,989,865,482,
# 	358,487,363,364,753,370,371,762,636,893,784]


lys_l = [989,1127,487,1227,1184,1188,1235,545]

model_resl = [int(l[22:26]) for l in open('T149_complex_1.pdb') if 'ATOM' in l[:4]]


lys_l = list(set(model_resl).intersection(lys_l))
resdic = dict([(r, 0) for r in lys_l])
model_dic = {}

out = open('xlink-dist.csv','w')
for f in glob.glob('*rsa'):
	pdb = f.replace('.rsa', '.pdb')

	counter = 0.
	lys_dic = {}
	for l in open(f).readlines()[4:-5]:
		data = l.split()
		resname = data[1]
		resnum = int(data[2])
		v = float(data[6])
		if resname == 'LYS' and resnum in lys_l and v >= 40.0:
			lys_dic[resnum] = v
			counter += 1
			resdic[resnum] += 1

	per = counter / float(len(lys_l))
	if per > 1.0:
		print 'what'
		exit()
	out.write('%s\t%.2f\t%i\t%i\n'% (pdb, per, counter, float(len(lys_l))))
out.close()

out = open('resdist.csv','w')
for e in resdic:
	tbw = '%i,%i\n' % (e, resdic[e])
	out.write(tbw)

out.close()
