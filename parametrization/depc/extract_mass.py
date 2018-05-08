# topology contains masses of the beads, try to get it from martini_v2.1P-dna.itp

reference_file = 'haddock-martini-bead-reference_4top.csv'

bead_dic = dict([(l.split(',')[0],l.split(',')[1].split('\n')[0]) for l in open(reference_file).readlines()])

# load all masses from martini file
mass_dic = {}
for l in open('martini_v2.1P-dna_masses.itp'):
	# print l
	data = l.split()
	bead = data[0]
	mass = float(data[2])
	mass_dic[bead] = mass

for e in bead_dic:
	haddock_bead = e
	martini_bead = bead_dic[e].split('\r')[0]
	#
	mass_value = mass_dic[martini_bead]
	#
	# print haddock_bead, martini_bead, mass_value
	print 'MASS %s %.2f' % (haddock_bead, mass_value)
