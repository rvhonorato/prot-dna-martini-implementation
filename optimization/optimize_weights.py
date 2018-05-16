# read output from optimization.dat

def find_key(dic, val):
	return [k for k, v in dic.iteritems() if v == val][0]

opt_d = {}
for l in open('optimization.dat'):
	data = l.split()
	auc = float(data[3])
	comb = l.split(':')[-1][1:-1]
	opt_d[comb] = auc


max_auc = max(opt_d.values())
max_comb = find_key(opt_d, max_auc)

min_auc = min(opt_d.values())
min_comb = find_key(opt_d, min_auc)

#
print max_auc, max_comb
print min_auc, min_comb

default_comb = '(1.0, 0.01, 1.0, 0.01)'


#( (E_elec * w1) + (E_vdw * w2) + (E_desolv * w3) + (BSA * w3) )

