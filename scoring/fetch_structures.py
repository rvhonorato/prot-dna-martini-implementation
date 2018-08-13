# find structures for visual inspection
import sys, os
# top1 model of top20 clusters
#f = sys.argv[1]

l = ['new-clusters-min4','new-clusters-min2']
os.system('mkdir ~/top20/min2')
os.system('mkdir ~/top20/min4')

for f in l:
	idx = int(f[-1])
	cluster_idxs = [e.split()[0] for e in open('%s/statistics' % f).readlines() if not '#' in e][:20]
	models = [(c, open('%s/file.nam_%s_best%i-scores' % (f, c, idx)).readlines()[2].split()[0]) for c in cluster_idxs]
	# print 'pymol %s' % ' '.join([p[1] for p in models])

	for m in models:
		new_name = 'c' + m[0].split('clust')[-1] + '_' + m[1]
		os.system('cp %s ~/top20/min%i/%s' % (m[1], idx, new_name))
		print m
