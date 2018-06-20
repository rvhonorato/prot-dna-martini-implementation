# extract nonbonded parameters from the martini ff
import itertools

def find_key(dic, val):
	'''return the key of dictionary dic given the value'''
	return [k for k, v in dic.iteritems() if v == val][0]

# reference_file = 'haddock-martini-full-bead-reference.csv'
# reference_file = 'haddock-martini-full-bead-reference_wRNA.csv'
# bead_dic = dict([(l.split(',')[0],l.split(',')[1].split('\n')[0].split('\r')[0]) for l in open(reference_file).readlines()[1:]])

# haddock-martini
bead_dic = {
'NH1':'TA2',
'NH2':'TA3',
'NH3':'TG2',
'NH4':'TG3',
'NH5':'TT2',
'NH6':'TT3',
'NH7':'TY2',
'NH8':'TY3',
'RH1':'TA2',
'RH2':'TA3',
'RH7':'TY2',
'RH8':'TY3',
'RH3':'TG2',
'RH4':'TG3',
'RH5':'TT2',
'RH6':'TT3',
'NB1':'Q0',
'NB2':'SN0',
'NB3':'SC2',
'ANS1':'TN0',
'ANS1':'TN0',
'ANS3':'TP1',
'ANS2':'TNa',
'NB1':'Q0',
'NB2':'SN0',
'NB3':'SC2',
'CNS1':'TN0',
'CNS4':'TP2',
'CNS3':'TP1',
'NB1':'Q0',
'NB2':'SN0',
'NB3':'SC2',
'GNS1':'TN0',
'GNS3':'TP1',
'GNS4':'TP2',
'GNS2':'TNa',
'NB1':'Q0',
'NB2':'SN0',
'NB3':'SC2',
'TNS1':'TN0',
'TNS4':'TP2',
'TNS2':'TNa',
'RNB1':'Q0',
'RNB2':'SN0',
'RNB3':'SNda',
'ARS1':'TN0',
'ARS1':'TN0',
'ARS2':'TP1',
'ARS3':'TNa',
'RNB1':'Q0',
'RNB2':'SN0',
'RNB3':'SNda',
'CRS1':'TN0',
'CRS4':'TP2',
'CRS3':'TP1',
'RNB1':'Q0',
'RNB2':'SN0',
'RNB3':'SNda',
'GRS1':'TN0',
'GRS3':'TP1',
'GRS4':'TP2',
'GRS2':'TNa',
'RNB1':'Q0',
'RNB2':'SN0',
'RNB3':'SNda',
'URS1':'TN0',
'URS4':'TP2',
'URS2':'TNa'}


# read all martini information into a dictionary
nonbonded_dic = dict([((l.split()[0], l.split()[1]), (float(l.split()[3]), float(l.split()[4]))) for l in open('/Users/rvhonorato/alc/Nostromo/parametrization/nonbonded-subset.dat')])

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
# out = open('self-crossterms.params','w')
# out.write('%s\n\n%s' % ('\n'.join(selfterms), '\n'.join(crossterms)))
# out.close()
