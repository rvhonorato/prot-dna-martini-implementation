# extract information from runX/itX.dat as a nice dataframe for R plots

import glob, os
import pandas as pd

ls = glob.glob('*/')
ls.sort()

phases = ['it0', 'it1', 'water']
# run_l = ['run1', 'run2']

run_ref = dict([(int(r.split('run')[-1].split('/')[0]), range(8,20,1)[int(r.split('run')[-1].split('/')[0])-1]) for r in ls])


for p in phases:
	data_dic = {}
	for run in ls:

		run_n = int(run.split('run')[-1].split('/')[0])
		threshold = run_ref[run_n]
		data_f = '%s%s.dat' % (run, p)

		if os.path.isfile(data_f):
			# print data_f
			data_dic[threshold] = []
			for l in open(data_f).readlines()[1:]:
				irms = float(l.split('\t')[6])
				data_dic[threshold].append(irms)
	#
	df = pd.DataFrame.from_dict(data_dic)
	df.to_csv('%s_threshold.csv' % p)

		# r = max([len(data_dic[d]) for d in data_dic])
		# exit()
		# if run == 'run1':
		# 	out = open('%s_cg_bench.dat' % p,'w')
		# else:
		# 	out = open('%s_aa_bench.dat' % p,'w')

		# out.write('\t'.join(['"%s"' % h for h in data_dic.keys()]) + '\n')

		# for i in range(0, r):
		# 	tbw = ''
		# 	for f in data_dic:
		# 		tbw += '%.2f\t' % data_dic[f][i]
		# 	out.write(tbw[:-1]+'\n')

		# out.close()