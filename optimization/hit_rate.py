# calculate the success rate
#
# how many complex have at least 1 model in topX
import glob, os, sys


def calc_sucess(file_list, topN, tag):
	hit_count = 0.
	total = float(len(file_list))
	# score_dic = {}
	for f in file_list:
		# hit_count = 0.
		# score_dic[f] = []
		for l in open(f).readlines()[1:topN+1]:
			data = l.split()
			rank = int(data[2])
			irmsd = float(data[6])
			#
			if irmsd <= 4.0:
				hit_count += 1
				# score_dic[f].append(1)
				# break
	per = hit_count / (topN * total)
	return per
	# print topN, per

phase = ['it0','it1','water']

for p in phase:
	file_listCG = glob.glob('*/run1/%s.dat' % p)
	file_listAA = glob.glob('*/run2/%s.dat' % p)

	cg_names = [e.split('/')[0] for e in file_listCG]
	aa_names = [e.split('/')[0] for e in file_listAA]

	cg_file_list = ['%s/run1/%s.dat' % (e,p) for e in list(set(cg_names) & set(aa_names))]
	aa_file_list = ['%s/run2/%s.dat' % (e,p) for e in list(set(cg_names) & set(aa_names))]

	top_l = [1,4,10,15,20,25,100,200]
	# top_l = [1,2,4,10]


	d = {}
	for t in top_l:
		cgper = calc_sucess(cg_file_list, t, 'CG')
		aaper = calc_sucess(aa_file_list, t, 'AA')
		# print '-'*20
		d[t] = cgper, aaper

	import matplotlib.pyplot as plt
	import pandas as pd
	df = pd.DataFrame.from_dict(d)
	df.to_csv('hitrate_%s.csv' % p)