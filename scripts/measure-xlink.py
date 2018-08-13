# measure xlink distances
import sys, glob
import numpy as np
lys_l = [989,1127,487,1227,1184,1188,1235,545]

model_dic = {}
for ident, l in enumerate(open('file.nam').readlines()):
	model_dic[ident+1] = l

cluster_dic = {}
for l in open('analysis/cluster.out'):
	data = l.split()
	cluster_n = data[1]
	cluster_idx = map(int, data[3:])
	cluster_dic[cluster_n] = [model_dic[c].split('\n')[0] for c in cluster_idx]


for c in cluster_dic:
	pdb_l = cluster_dic[c]
	counter_l = []
	counter_dic = dict([(k, 0.0) for k in lys_l])
	for p in pdb_l:
		lys_d = dict([(e, []) for e in lys_l])
		# get coords
		for l in open(p).readlines():
			if 'ATOM' in l[:4] and int(l[22:26]) in lys_l and 'CA' in l[12:16]:
				x = float(l[31:38])
				y = float(l[38:46])
				z = float(l[46:54])
				chain = l[21]
				resnum = int(l[22:26])
				lys_d[resnum].append((x,y,z))

		counter = 0
		for r in lys_d:
			A, B = lys_d[r]
			dist = np.linalg.norm(np.array(A)-np.array(B))
			if dist <= 30:
				counter += 1
				counter_dic[r] += 1
		score = float(counter) / float(len(lys_l))
		counter_l.append(score)
	print 'cluster %i %.2f %%\n' % (int(c), np.mean(counter_l)*100), 

	for k in counter_dic:
		print 'xlink: %i - %.2f %%' % (k, (counter_dic[k] / float(len(pdb_l)))*100)

	# counter_dic / float(len(pdb_l))#, np.array(counter_l)*100

