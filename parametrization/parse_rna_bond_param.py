# this information is derived from the papers!
# S3 in RNA

# special hydrogen bonding beads have the same parameters 
#  as the non bonding ones

# MARTINI BEAD TYPE , HADDOCK BEAD
bead_ref = {
'BB1': ['RNB1'],
'BB2': ['RNB2'],
'BB3': ['RNB3'],

'ASC1':['ARS1'],
'ASC2':['ARS2','RH1'],
'ASC3':['ARS3','RH2'],
'ASC4':['ARS4'],

'CSC1':['CRS1'],
'CSC2':['CRS2','RH7'],
'CSC3':['CRS3','RH8'],

'GSC1':['GRS1'],
'GSC2':['GRS2','RH3'],
'GSC3':['GRS3','RH4'],
'GSC4':['GRS4'],

'USC1':['URS1'],
'USC2':['URS2','RH5'],
'USC3':['URS3','RH6']}

bond_dic = {
('BB1','BB2'): (0.363, 20000),
('BB2','BB3'): (0.202, 40000),
('BB3','BB1'): (0.354, 10000),

('BB3','ASC1'): (0.293, 28000),
('ASC1','ASC2'): (0.234, 'constraint'),
('ASC2','ASC3'): (0.263, 'constraint'),
('ASC2','ASC4'): (0.335, 40000),
('ASC3','ASC4'): (0.299, 'constraint'),
('ASC4','ASC1'): (0.162, 'constraint'),

('BB3','CSC1'): (0.280, 11000),
('CSC1','CSC2'): (0.224, 'constraint'),
('CSC2','CSC3'): (0.281, 'constraint'),
('CSC3','CSC1'): (0.267, 'constraint'),

('BB3','GSC1'): (0.292, 20000),
('GSC1','GSC2'): (0.296, 'constraint'),
('GSC2','GSC3'): (0.291, 'constraint'),
('GSC2','GSC4'): (0.385, 40000),
('GSC3','GSC4'): (0.296, 'constraint'),
('GSC4','GSC1'): (0.162, 'constraint'),

('BB3','USC1'): (0.286, 18000),
('USC1','USC2'): (0.224, 'constraint'),
('USC2','USC3'): (0.289, 'constraint'),
('USC3','USC1'): (0.276, 'constraint')}

for e in bond_dic:
	l, eps = bond_dic[e]
	l = l*10
	if eps == 'constraint':
		eps = 500.
	else:
		eps = eps/417.8
	bA, bB = e
	#
	# print e
	for a in bead_ref[bA]:
		for b in bead_ref[bB]:
			#
			print 'BOND %s %s\t%.3f\t%.3f' % (a, b, eps, l)