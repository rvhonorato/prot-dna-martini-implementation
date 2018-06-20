# extract information from runX/itX.dat as a nice dataframe for R plots

import glob, os

ls = glob.glob('*/')


phases = ['it0', 'it1', 'water']
run_l = ['run1', 'run2']

for p in phases:
	for run in run_l:
		data_dic = {}
		for f in ls:
			data_f = '%s%s/%s.dat' % (f,run, p)
			data_dic[f.split('/')[0]] = []
			if os.path.isfile(data_f):
				for l in open(data_f).readlines()[1:]:
					irms = float(l.split('\t')[6])
					data_dic[f.split('/')[0]].append(irms)

		# remove empty entries
		data_dic = dict((k, v) for k, v in data_dic.iteritems() if v)

		r = max([len(data_dic[d]) for d in data_dic])
		exit()
		if run == 'run1':
			out = open('%s_cg_bench.dat' % p,'w')
		else:
			out = open('%s_aa_bench.dat' % p,'w')

		out.write('\t'.join(['"%s"' % h for h in data_dic.keys()]) + '\n')

		for i in range(0, r):
			tbw = ''
			for f in data_dic:
				tbw += '%.2f\t' % data_dic[f][i]
			out.write(tbw[:-1]+'\n')

		out.close()