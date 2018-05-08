# irmsd,haddockscore,irmsd,haddockscore,irmsd,haddockscore || pdb1\npdb2\npdb3
import glob, os

ls = glob.glob('*/')
#ls = ['1B3T/','1DDN/']

# loc = [run1/it0.dat]

r_dic = {}
for f in ls:
	data_f = '%srun1/it1.dat' % f
	if os.path.isfile(data_f):
		values = [(float(l.split('\t')[6]), float(l.split('\t')[3])) for l in open(data_f).readlines()[1:]]
		r_dic[f.split('/')[0]] = values

v_len = max([len(r_dic[e]) for e in r_dic])

out = open('minput.txt','w')
for i in range(0, v_len):
	tbw = ''
	for f in r_dic:
		tbw += '%.2f\t%.2f\t' % (r_dic[f][i][0], r_dic[f][i][1])
	#
	out.write(tbw[:-1]+'\n')
out.close()

out = open('codes.txt','w')
for f in r_dic:
	out.write('%s\n' % f)
out.close()


# for f in r_dic:


# 3 score
# 6 irms
