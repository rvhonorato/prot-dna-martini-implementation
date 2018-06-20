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

# for p in phase:
p = 'it0'
file_listCG = glob.glob('*/run1/%s.dat' % p)
file_listAA = glob.glob('*/run2/%s.dat' % p)
# exit()
cg_names = [e.split('/')[0] for e in file_listCG]
aa_names = [e.split('/')[0] for e in file_listAA]

cg_file_list = ['%s/run1/%s.dat' % (e,p) for e in list(set(cg_names) & set(aa_names))]
aa_file_list = ['%s/run2/%s.dat' % (e,p) for e in list(set(cg_names) & set(aa_names))]

# top_l = [1,4,10,15,20,25,100,200]
top_l = [4]
# top_l = [1,2,4,10]

# out = open('sucess.debug','w')
d = {}
import numpy as np
for topN in top_l:
	d[topN] = np.array([float('nan')]*200*38)
	# tbw = '%i\t' %topN
	# tbw = ''
	counter = 0
	for f in cg_file_list:
		# counter = 0
		#
		size = len(open(f).readlines()[1:topN+1])
		#
		f_m_name = open(f).readlines()[1:topN+1][0].split('\t')[1].split('/')[-1]
		f_m_rank = open(f).readlines()[1:topN+1][0].split('\t')[2]
		f_m_irmsd = open(f).readlines()[1:topN+1][0].split('\t')[6]
		#
		l_m_name = open(f).readlines()[1:topN+1][-1].split('\t')[1].split('/')[-1]
		l_m_rank = open(f).readlines()[1:topN+1][-1].split('\t')[2]
		l_m_irmsd = open(f).readlines()[1:topN+1][-1].split('\t')[6]
		#
		print size, f_m_name, f_m_rank, f_m_irmsd, l_m_name, l_m_rank, l_m_irmsd
		#
		# counter = 0
		name = f.split('/')[0]
		for i, l in enumerate(open(f).readlines()[1:topN+1]):
			data = l.split('\t')
			irmsd = float(data[6])
			# tbw += '%.2f,' % irmsd
			# d[topN].append(irmsd)
			d[topN][counter] =irmsd
			counter += 1
			# print topN, i, irmsd

import pandas as pd
df = pd.DataFrame.from_dict(d)
df.to_csv('sucess.debug',sep=' ', index=False)
	# print tbw
	# exit()
	# out.write(tbw[:-1] + '\n')

# out.close()
			# name = data[1].split('/')[-1]
			# if irmsd <= 4.0:
				# counter += 1
				# d[name] = 1
	#
	# print topN, float(len(d)) / float(len(cg_file_list)) * 100


		# print , , open(f).readlines()[1:topN+1][0].split('\t')[2], open(f).readlines()[1:topN+1][-1].split('\t')[1], open(f).readlines()[1:topN+1][-1].split('\t')[2]

exit()
# 	for l in open(f).readlines()[1:topN+1]:
# 		data = l.split()
# 		rank = int(data[2])
# 		irmsd = float(data[6])
# 		#
# 		if irmsd <= 4.0:
# 			hit_count += 1
# 			# score_dic[f].append(1)
# 			# break
# per = hit_count / (topN * total)
# return per

	# cgper = calc_sucess(cg_file_list, t, 'CG')
	# aaper = calc_sucess(aa_file_list, t, 'AA')
	# print '-'*20
	# d[t] = cgper, aaper

import matplotlib.pyplot as plt
import pandas as pd
df = pd.DataFrame.from_dict(d)
df.to_csv('hitrate_%s.csv' % p)