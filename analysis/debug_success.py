import glob, os

ls = glob.glob('*/')
data_dic = {}
for f in ls:
	pdbname = f.split('/')[0]
	dataf = '%srun1/it0.dat' % f
	if os.path.isfile(dataf):
		# data_dic[pdbname] = {}
		data = open(dataf).readlines()[1].split('\t')
		# data = l.split('\t')
		rank = int(data[2])
		irms = float(data[6])
		#
		print '%s %.2f' % (pdbname, irms)
		# for l in open(dataf).readlines()[1:]: