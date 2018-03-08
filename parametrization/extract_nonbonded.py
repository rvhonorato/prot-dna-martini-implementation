# extract nonbonded parameters from the martini ff

def find_key(dic, val):
	'''return the key of dictionary dic given the value'''
	return [k for k, v in dic.iteritems() if v == val][0]

reference_file = 'haddock-martini-dna-bead-reference_4top.csv'

bead_dic = dict([(l.split(',')[0],l.split(',')[1].split('\n')[0].split('\r')[0]) for l in open(reference_file).readlines()[1:]])

for l in open('martini_v2.1P-dna_nonbonded.itp'):
	data = l.split()
	martini_beadA = data[0]
	martini_beadB = data[1]
	_ = data[2]
	v1 = float(data[3])
	v2 = float(data[4])
	#
	# check if these beads are in the dictionary
	try:
		haddock_beadA = find_key(bead_dic, martini_beadA)
		haddock_beadB = find_key(bead_dic, martini_beadB)
	except:
		continue
	print haddock_beadA, haddock_beadB, v1, v2
