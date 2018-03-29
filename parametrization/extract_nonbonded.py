# extract nonbonded parameters from the martini ff
import itertools

def find_key(dic, val):
	'''return the key of dictionary dic given the value'''
	return [k for k, v in dic.iteritems() if v == val][0]

reference_file = 'haddock-martini-full-bead-reference.csv'

bead_dic = dict([(l.split(',')[0],l.split(',')[1].split('\n')[0].split('\r')[0]) for l in open(reference_file).readlines()[1:]])


# read all martini information into a dictionary
nonbonded_dic = dict([((l.split()[0], l.split()[1]), (float(l.split()[3]), float(l.split()[4]))) for l in open('martini_v2.1P-dna_nonbonded.itp')])

# generate all bead combinations
bead_combinations = itertools.combinations(bead_dic.keys(), 2)

# get self terms
selfterms = []
for haddock_bead in bead_dic:
	martini_bead = bead_dic[haddock_bead]
	#
	sigma, epsilon = nonbonded_dic[(martini_bead, martini_bead)]
	sig = sigma * 10 # nm to aa
	eps = epsilon / 4.178 # kJ to kCal
	#
	print 'NONBONded\t%s\t%.3f\t%.1f\t%.3f\t%.1f' % (haddock_bead, sig, eps, sig, eps)
	# selfterms.append('NONBONded\t%s\t%.3f\t%.1f\t%.3f\t%.1f' % (haddock_bead, sig, eps, sig, eps))


# get crossterms
crossterms = []
for e in bead_combinations:
	#
	haddock_beadA = e[0]
	haddock_beadB = e[1]
	#
	martini_beadA = bead_dic[haddock_beadA]
	martini_beadB = bead_dic[haddock_beadB]
	#
	try:
		v = nonbonded_dic[(martini_beadA, martini_beadB)]
	except KeyError:
		v = nonbonded_dic[(martini_beadB, martini_beadA)]
	#	
	sigma, epsilon = v
	#
	attr = (4 * (sigma*10)**12) * (epsilon / 4.178) # cns takes of the rest of the formula
	rep = (4 * (sigma*10)**6) * (epsilon / 4.178) # cns takes care of the rest of the formula
	if any( [attr, rep] ):
		# crossterms.append('NBFIx\t%s\t%s\t%.3f\t%.3f\t%.3f\t%.3f' % (haddock_beadA, haddock_beadB, attr, rep, attr, rep))
		print 'NBFIx\t%s\t%s\t%.3f\t%.3f\t%.3f\t%.3f' % (haddock_beadA, haddock_beadB, attr, rep, attr, rep)


# format!
out = open('self-crossterms.params','w')
out.write('%s\n\n%s' % ('\n'.join(selfterms), '\n'.join(crossterms)))
out.close()
