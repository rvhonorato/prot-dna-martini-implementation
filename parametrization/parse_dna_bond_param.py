# this information is derived from the papers!
# S1 in DNA

# special hydrogen bonding beads have the same parameters 
#  as the non bonding ones

# MARTINI BEAD TYPE - HADDOCK BEAD
bead_ref = {
'BB1': ['NB1'],	
'BB2': ['NB2'],	
'BB3': ['NB3'],
'BB4': ['NB4'],	

'ASC1': ['ANS1'],
'ASC2': ['ANS1', 'NH1'],
'ASC3': ['ANS3', 'NH2'],
'ASC4': ['ANS2'],
		
'GSC1': ['GNS1'],
'GSC2': ['GNS3', 'NH3'],
'GSC3': ['GNS4', 'NH4'],
'GSC4': ['GNS2'],
		
'CSC1': ['CNS1'],
'CSC2': ['CNS4','NH7'],
'CSC3': ['CNS3','NH8'],
		
'TSC1': ['TNS1'],
'TSC2': ['TNS4', 'NH5'],
'TSC3': ['TNS2', 'NH6'],

}

bond_dic = {
('BB1','BB2'): (0.360, 20000),
('BB2','BB3'): (0.198, 80000),
('BB3','BB1'): (0.353, 10000),

('BB3','ASC1'): (0.300, 30000),
('ASC1','ASC2'): (0.229, 'constraint'),
('ASC2','ASC3'): (0.266, 'constraint'),
('ASC2','ASC4'): (0.326, 20000),

('ASC3','ASC4'): (0.288, 'constraint'),
('ASC4','ASC1'): (0.162, 'constraint'),

('BB3','CSC1'): (0.270, 30000),
('CSC1','CSC2'): (0.220, 'constraint'),
('CSC2','CSC3'): (0.285, 'constraint'),
('CSC3','CSC1'): (0.268, 'constraint'),

('BB3','GSC1'): (0.300, 30000),
('GSC1','GSC2'): (0.295, 'constraint'),
('GSC2','GSC3'): (0.295, 'constraint'),
('GSC2','GSC4'): (0.389, 20000),
('GSC3','GSC4'): (0.285, 'constraint'),
('GSC4','GSC1'): (0.161, 'constraint'),

('BB3','TSC1'): (0.270, 30000),
('TSC1','TSC2'): (0.217, 'constraint'),
('TSC2','TSC3'): (0.322, 'constraint'),
('TSC3','TSC1'): (0.265, 'constraint')
}

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
			 # F4 F4   500 3.500











