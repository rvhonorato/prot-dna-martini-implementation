# get the clusters for a run
#  mean scores for top4 of each cluster
#  rank
#  success rate

import gzip, operator, glob, os
import pandas as pd

ls = [p for p in glob.glob('*') if not '.' in p and p != 'plots']
# runn = 4

runL = [3,4]
topL = [1, 5, 10, 50, 100, 200]



# phase_dic ={
	# 'water': ['structures/it1/water/file.list', 'structures/it1/water/analysis/cluster.out.gz', 'structures/it1/water/i-RMSD.dat'],
	# 'it0': ['structures/it1/file.list', 'structures/it1/analysis/cluster.out.gz', 'structures/it1/i-RMSD.dat'],
	# 'it1': ['structures/it0/file.list', 'structures/it0/analysis/cluster.out.gz', 'structures/it0/i-RMSD.dat']}

# for phase in phase_dic:

for runn in runL:
	print '#'*10,runn
	success_dic = dict([(e, [.0,.0,.0]) for e in topL])
	for target in ls:

		# score_f = '%s/run%i/%s' % (target, runn, phase_dic[phase][0])
		# cluster_f = '%s/run%i/%s' % (target, runn, phase_dic[phase][1])
		# irmsd_f = '%s/run%i/%s' % (target, runn, phase_dic[phase][2])

		score_f = '%s/run%i/structures/it1/water/file.list' % (target, runn)
		cluster_f = '%s/run%i/structures/it1/water/analysis/cluster.out.gz' % (target, runn)
		irmsd_f = '%s/run%i/structures/it1/water/i-RMSD.dat' % (target, runn)

		score_dic = dict([(i+1,float(l.split()[-2])) for i, l in enumerate(open(score_f))])
		model_dic = dict([(i+1,l.split()[0].split(':')[-1][:-1]) for i, l in enumerate(open(score_f))])
		irmsd_dic = dict([(l.split()[0], float(l.split()[1])) for l in open(irmsd_f).readlines()[1:]])

		if not os.path.isfile(cluster_f):
			cluster_f = '%s/run%i/structures/it1/water/analysis/cluster.out' % (target, runn)
			cluster_data=open(cluster_f)
		else:
			cluster_data=gzip.open(cluster_f)


		c_dic = {}
		cluster_model_dic = {}
		for c in cluster_data:
			cluster_idx = int(c.split()[1])
			center = c.split()[3]
			top4 = map(int, c.split()[4:8])
			#
			mean_cluster_score = sum([score_dic[e] for e in top4]) / 4.0
			c_dic[cluster_idx] = mean_cluster_score
			cluster_model_dic[cluster_idx] = map(int, c.split()[3:])

		sorted_c_dic = sorted(c_dic.items(), key=operator.itemgetter(1))
		top_cluster = sorted_c_dic[0][0]

		top_models = [model_dic[p] for p in cluster_model_dic[top_cluster]]

		# get i-rmsd for this models
		irmsd_l = [irmsd_dic[e] for e in top_models]

		for topN in topL:

			if any([v <= 4.0 for v in irmsd_l[:topN]]):
				success_dic[topN][0] += 1
			if any([v <= 2.0 for v in irmsd_l[:topN]]):
				success_dic[topN][1] += 1
			if any([v <= 1.0 for v in irmsd_l[:topN]]):
				success_dic[topN][0] += 1
	per_dic = {}
	for t in success_dic:
		per_dic[t] = [(e/float(len(ls)))*100 for e in success_dic[t]]

	df = pd.DataFrame.from_dict(per_dic)
	df.to_csv('run%i_water_cluster_success_rate.csv' % (runn))



