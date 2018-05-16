import glob, os, gzip

ls = glob.glob('*/')


phases = ['it0', 'it1']
run_l = ['run1', 'run2']

for p in phases:
	for r in run_l:
		data_dic = {}
		for f in ls:
			fname = f.split('/')[0]
			if r == 'run1':
				data_f = '%srun1/%s_%s_%s_refine_1.out.gz' % (f, fname, r, p)
			else:
				data_f = '%srun2/complex_run1_%s_refine_1.out' % (f, p)

			
			if os.path.isfile(data_f):
				# if r == 'run1':
				try:
					cpu_time = float(gzip.open(data_f).readlines()[-2].split()[3])
				except:
					cpu_time = float(open(data_f).readlines()[-2].split()[3])
				data_dic[fname] = cpu_time

		if r == 'run1':
			out = open('%s_cg_cpu_bench.dat' % p,'w')
		else:
			out = open('%s_aa_cpu_bench.dat' % p,'w')

		out.write('\t'.join([h for h in data_dic.keys()]) + '\n')

		tbw = ''
		for f in data_dic:
			tbw += '%.2f\t' % data_dic[f]

		out.write(tbw[:-1]+'\n')
		out.close()

# extra round, get complexes size
out = open('p_size.dat','w')
out.write('complex\tatomcount\n')
# for p in phases:
	# for r in run_l:
for f in ls:
	fname = f.split('/')[0]
	try:
		pdb = glob.glob('%s/run1/structures/it1/water/*pdb' % (fname))[0]
	# if os.path.isfile(pdb):
		atomcount = len(open(pdb).readlines())
		out.write('%s\t%i\n' % (fname, atomcount))
	except:
		pass

out.close()








