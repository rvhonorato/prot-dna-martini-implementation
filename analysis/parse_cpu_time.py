import glob, os, gzip, sys, argparse


parser = argparse.ArgumentParser()

parser.add_argument("runn", type=int,
                    help="Run number")

parser.add_argument("--local", 
					help="Consider local naming scheme",
                    action="store_true")

args = parser.parse_args()

run = 'run%i' % args.runn
# tag_l = ['act-pass', 'act-pass-nodesol','CM', 'CM-nodesol']
ls = glob.glob('*/')

phases = ['it0', 'it1']

for p in phases:
	data_dic = {}
	# for tag in tag_l:
	for f in ls:

		fname = f.split('/')[0]
		# run = '%s-%s' % (fname,tag)

		if args.local:
			# 1A74_run1_it0_refine_1.out.gz
			data_f = '%s/%s/%s_%s_%s_refine_1.out.gz' % (fname, run, fname, run, p)
		else:
			data_f = '%s/%s/complex_run1_%s_refine_1.out' % (fname, run, p)

		if os.path.isfile(data_f):
			if args.local:
				cpu_time = float(gzip.open(data_f).readlines()[-2].split()[3])
			else:
				cpu_time = float(open(data_f).readlines()[-2].split()[3])

			data_dic[fname] = cpu_time

	out = open('%s_%s_cpu_bench.dat' % (run, p),'w')
	# out = open('/home/rodrigo/%s_%s_cpu_bench.dat' % (tag, p),'w')
	out.write('\t'.join([h for h in data_dic.keys()]) + '\n')
	tbw = ''
	for f in data_dic:
		tbw += '%.2f\t' % data_dic[f]
	out.write(tbw[:-1]+'\n')
	out.close()

# extra round, get complexes size
out = open('%s_p_size.dat' % run,'w')
out.write('complex\tatomcount\n')
for f in ls:
	fname = f.split('/')[0]
	try:
		pdb = glob.glob('%s/%s/structures/it1/water/*pdb' % (fname, run))[0]
		atomcount = len(open(pdb).readlines())
		out.write('%s\t%i\n' % (fname, atomcount))
	except:
		pass

out.close()








