# read result table and get percentages
import os, sys


#'stage\tpdb_name\trank\tscore\tfnat\tlrms\tirms\tbinding\tdesolv\tbinding\ttotal\tbonds\tangles\timproper\tdihe\tvdw\telec\tair\tcdih\tcoup\trdcs\tvean\tdani\txpcs\trg\n'
# categorize
target_f = ['it0.dat', 'it1.dat', 'water.dat']

for f in target_f:
	category_dic = {'high': 0, 'medium': 0, 'acceptable': 0}
	for l in open(f).readlines()[1:]:
		data = l.split()
		# print data
		pdb = data[1]
		fnat = float(data[4])
		lrms = float(data[5])
		irms = float(data[6])
		print fnat, lrms, irms
		#
		if fnat > 0.5 and irms < 1.0 and lrms < 1.0:
			category_dic['high'] += 1
		elif fnat > 0.3 and lrms < 5.0 and irms < 1.0:
			category_dic['medium'] += 1
		elif fnat > 0.1 and lrms < 10.0 and irms < 4.0:
			category_dic['acceptable'] += 1
	#
	print f, category_dic
# print l