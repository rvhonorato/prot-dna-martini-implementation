# from a csv copied form the paper, parse and output the parameters
import itertools

def find_keys(dic, val):
	'''return the key of dictionary dic given the value'''
	return [k for k, v in dic.iteritems() if v == val]

atom_base_bead_ref = {
'SC1':'TN0', 
'SC2':'TA2', 
'SC3':'TA3', 
'SC4':'TNa', 
'SC1':'TN0', 
'SC2':'TY2', 
'SC3':'TY3', 
'SC1':'TN0', 
'SC2':'TG2', 
'SC3':'TG3', 
'SC4':'TNa', 
'SC1':'TN0', 
'SC2':'TT2', 
'SC3':'TT3'
}
# expand to fit each base
atom_bead_ref = dict([((a + b), atom_base_bead_ref[b]) for b in atom_base_bead_ref for a in ['A','C','T','G']])
atom_bead_ref['BB1'] = 'Q0' 
atom_bead_ref['BB2'] = 'SN0' 
atom_bead_ref['BB3'] = 'SC2'

reference_file = 'haddock-martini-full-bead-reference.csv'
bead_dic = dict([(l.split(',')[0],l.split(',')[1].split('\n')[0].split('\r')[0]) for l in open(reference_file).readlines()[1:]])



bonds = []
angles = []
dih = []

for l in open('bond_angles_dihedrals.csv'):
	bead_list, entry_type, value, force_constant = l.split(' ')
	#
	try:
		force = float(force_constant) / 417.8
	except:
		force = 500.
	#
	# force_constant = force_constant / 417.8 # make it kcal/mol A2
	#
	idx = bead_list.count('-')
	bead_list = bead_list.split('-')
	martini_bead_list = [atom_bead_ref[b] for b in bead_list]
	#
	# generate all combinations...!
	haddock_beads = []
	c = 0
	for bead, mbead in zip(bead_list, martini_bead_list):
		# which haddock beads to these correlate to?
		possible_hbeads = find_keys(bead_dic, mbead)
		# filter based on nucleotide
		if not 'BB' in bead:
			nucleotide_idx = bead[0]
			selected_hbeads = [b for b in possible_hbeads if nucleotide_idx.lower() in b]
		else:
			selected_hbeads = possible_hbeads

		selected_hbeads.sort()
		haddock_beads.insert(c, selected_hbeads)
		c += 1
	#
	# print bead_list
	# print martini_bead_list
	# print haddock_beads
	#
	haddock_combinations = list(itertools.product(*haddock_beads))
	#
	if idx == 3:
		# print 'dih'
		degree = float(value)
		dih += ['DIHEdral %s %s %s %s\t%.2f\t%i\t%i' % (a, b, c, d, force, int(entry_type), degree) for (a, b, c, d) in haddock_combinations]
	#	
	if idx == 2:
		degree = float(value)
		angles += ['ANGLe\t%s\t%s\t%s\t%.2f\t%i' % (a, b, c, force, degree) for (a, b, c) in haddock_combinations]
	#
	if idx == 1:
		lenght = float(value) * 10 # value here is len
		bonds += ['BOND\t%s\t%s\t%.2f\t%.2f' % (a, b, force, lenght) for (a, b) in haddock_combinations]

# output!
out = open('bonds-angles-dih.param','w')
out.write('\n'.join(bonds))
out.write('\n\n')
out.write('\n'.join(dih))
out.write('\n\n')
out.write('\n'.join(angles))
out.close()
