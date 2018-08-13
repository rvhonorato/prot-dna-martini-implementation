# get top1 models from top10
import sys, os
# f = sys.argv[1]

f = '../rescored/new-clusters-min2/statistics'

out = open('top10.list','w')
for i, l in enumerate(open(f).readlines()[5:]):
	if i < 10:
		clustn = int(l.split()[0].split('clust')[-1])
		clustf = '../rescored/new-clusters-min2/file.nam_clust%i_best2-scores' % clustn
		pdbn = open(clustf).readlines()[1].split()[0]
		# open(clus)
		print i, clustn, pdbn
		out.write('%s\n' % pdbn)
		os.system('cp ../rescored/%s .' % pdbn)
		# print i, l, clustn

out.close()

