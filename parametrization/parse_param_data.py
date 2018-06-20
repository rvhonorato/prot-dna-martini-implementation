
dna_bead_ref = {
'BB1': ['NB1'],'BB2': ['NB2'],'BB3': ['NB3'],	
'ASC1': ['ANS1'],'ASC2': ['ANS1','NH1'],'ASC3': ['ANS3','NH2'],'ASC4': ['ANS2'],
'GSC1': ['GNS1'],'GSC2': ['GNS3','NH3'],'GSC3': ['GNS4','NH4'],'GSC4': ['GNS2'],
'CSC1': ['CNS1'],'CSC2': ['CNS4','NH7'],'CSC3': ['CNS3','NH8'],	
'TSC1': ['TNS1'],'TSC2': ['TNS4','NH5'],'TSC3': ['TNS2','NH6']}

rna_bead_ref = {
'BB1': ['RNB1'],'BB2': ['RNB2'],'BB3': ['RNB3'],
'ASC1': ['ARS1'],'ASC2': ['ARS1','RH1'],'ASC3': ['ARS2','RH2'],'ASC4': ['ARS3'],

'GSC1': ['GRS1'],'GSC2': ['GRS3','RH3'],'GSC3': ['GRS4','RH4'],'GSC4': ['GRS2'],

'CSC1': ['CRS1'],'CSC2': ['CRS4','RH7'],'CSC3': ['CRS3','RH8'],

'USC1': ['URS1'],'USC2': ['URS4','RH5'],'USC3': ['URS2','RH6']}

########################################
# ANGLES
########################################
dna_angle_dic = {
('BB1','BB2','BB3'): (110.0,200),
('BB2','BB3','BB1'): (102.0,150),
('BB3','BB1','BB2'): (106.0,75),

('BB2','BB3','ASC1'): (94.0,250),
('BB3','ASC1','ASC2'): (160.0,200),
('BB3','ASC1','ASC4'): (140.0,200),
('ASC1','ASC2','ASC3'): (85.0,200),
('ASC1','BB3','BB1'): (158.0,200),
('ASC2','ASC1','ASC4'): (125.0,200),
('ASC2','ASC3','ASC4'): (74.0,200),
('ASC3','ASC4','ASC1'): (98.0,200),

('BB2','BB3','CSC1'):  (95.0,210),
('BB3','CSC1','CSC2'): (95.0,300),
('BB2','CSC1','CSC3'): (150.0,500),
('CSC1','BB3','BB1'): (180.0,30),
('CSC1','CSC2','CSC3'): (61.0,200),
('CSC2','CSC1','CSC3'): (71.0,200),
('CSC2','CSC3','CSC1'): (47.0,200),

('BB2','BB3','GSC1'): (94.5,250),
('BB3','GSC1','GSC2'): (137.0,300),
('BB3','GSC1','GSC4'): (130.0,250),
('GSC1','GSC2','GSC3'): (69.5,200),
('GSC1','BB3','BB1'): (157.0,150),
('GSC2','GSC1','GSC4'): (125.0,200),
('GSC2','GSC3','GSC4'): (84.0,200),
('GSC3','GSC4','GSC1'): (94.0,200),

('BB2','BB3','TSC1'): (92.0,220),
('BB3','TSC1','TSC2'): (107.0,300),
('BB2','TSC1','TSC3'): (145.0,400),
('TSC1','BB3','BB1'): (180.0,30),
('TSC1','TSC2','TSC3'): (55.0,100),
('TSC2','TSC1','TSC3'): (83.0,100),
('TSC2','TSC3','TSC1'): (42.0,100)
}

rna_angle_dic = {
('BB1','BB2','BB3'): (117.0, 175),
('BB2','BB3','BB1'): (95.0, 105),
('BB3','BB1','BB2'): (93.0, 75),

('BB2','BB3','ASC1'): (101.0, 260),
('BB2','BB3','CSC1'): (94.0, 230),
('BB2','BB3','GSC1'): (103.0, 260),
('BB2','BB3','USC1'): (95.0, 225),

('ASC1','BB3','BB1'): (160.0, 15),
('CSC1','BB3','BB1'): (130.0, 0.5),
('GSC1','BB3','BB1'): (170.0, 20),
('USC1','BB3','BB1'): (180.0, 5),

('BB3','ASC1','ASC2'): (153.0, 90),
('BB3','ASC1','ASC4'): (135.0, 185),
('BB3','CSC1','CSC2'): (103.0, 170),
('BB2','CSC1','CSC3'): (155.0, 100),
('BB3','GSC1','GSC2'): (129.0, 80),
('BB3','GSC1','GSC4'): (137.0, 120),
('BB3','USC1','USC2'): (99.0, 200),
('BB2','USC1','USC3'): (155.0, 100),


('ASC1','ASC2','ASC3'): (87.0, 200),
('ASC2','ASC1','ASC4'): (115.0, 200),
('ASC2','ASC3','ASC4'): (74.0, 200),
('ASC3','ASC4','ASC1'): (92.0, 200),
('CSC1','CSC2','CSC3'): (61.0, 200),
('CSC2','CSC1','CSC3'): (71.0, 200),
('CSC2','CSC3','CSC1'): (47.0, 200),
('GSC1','GSC2','GSC3'): (72.0, 200),
('GSC2','GSC1','GSC4'): (117.0, 200),
('GSC2','GSC3','GSC4'): (84.0, 200),
('GSC3','GSC4','GSC1'): (96.5, 200),
('USC1','USC2','USC3'): (55.0, 100),
('USC2','USC1','USC3'): (83.0, 100),
('USC2','USC3','USC1'): (42.0, 100)}


########################################
# BONDS
########################################
# DNA
dna_bond_dic = {
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

# RNA
rna_bond_dic = {
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


# DIH
# DNA
dna_dih_dic = {
('BB1','BB2','BB3','BB1'): (2,95.0,25),
('BB2','BB3','BB1','BB2'): (1,1803,2),
('BB3','BB1','BB2','BB3'): (9,85.0,2),
('BB3','BB1','BB2','BB3'): (9,160.0,2),

('BB1','BB2','BB3','ASC1'): (2,-90.0,20),
('BB2','BB3','ASC1','ASC2'): (2,-116.0,0.5),
('BB2','BB3','ASC1','ASC4'): (2,98.0,15),

('BB1','BB2','BB3','CSC1'): (2,-78.0,25),
('BB2','BB3','CSC1','CSC2'): (2,-90.0,20),
('BB2','BB3','CSC1','CSC3'): (2,-142.0,50),

('BB1','BB2','BB3','GSC1'): (2,-90.0,20),
('BB2','BB3','GSC1','GSC2'): (2,-117.0,1),
('BB2','BB3','GSC1','GSC4'): (2,92.0,15),

('BB1','BB2','BB3','TSC1'): (2,-75.0,40),
('BB2','BB3','TSC1','TSC2'): (2, -110.0,15),
('BB2','BB3','TSC1','TSC3'): (2,-145.0,65)}

# RNA
rna_dih_dic = {
('BB1','BB2','BB3','BB1'): (2, 0.0, 3.5),
('BB2','BB3','BB1','BB2'): (1, 0.0, 1),
('BB3','BB1','BB2','BB3'): (9, -10.0, 1.5),
('BB3','BB1','BB2','BB3'): (9, 10.0, 1.5),

('BB1','BB2','BB3','ASC1'): (2, 180.0, 1.5),
('BB1','BB2','BB3','CSC1'): (1, 55.0, 3),
('BB1','BB2','BB3','CSC1'): (2, -130.0, 1),
('BB1','BB2','BB3','GSC1'): (1, -20.0, 1),
('BB1','BB2','BB3','USC1'): (1, 0.0, 2),

('BB2','BB3','ASC1','ASC2'): (1, -40.0, 4),
('BB2','BB3','ASC1','ASC2'): (2, 180.0, 2),
('BB2','BB3','ASC1','ASC4'): (1, -10.0, 5),
('BB2','BB3','ASC1','ASC4'): (2, 80.0, 0.5),
('BB2','BB3','CSC1','CSC2'): (2, 180.0, 3),
('BB2','BB3','CSC1','CSC2'): (1, 0.0, 2),
('BB2','BB3','GSC1','GSC2'): (2, 180.0, 3.5),
('BB2','BB3','GSC1','GSC4'): (1, 0.0, 5),
('BB2','BB3','USC1','USC2'): (2, 180.0, 4),
('BB2','BB3','USC1','USC3'): (1, 0.0, 2),

('ASC1','ASC2','ASC3','ASC4'): (2, 0.0, 10),
('GSC1','GSC2','GSC3','GSC4'): (2, 0.0, 10)}

######

def parse_bonds(bond_dic, bead_ref):
	for e in bond_dic:
		l, eps = bond_dic[e]
		l = l*10
		if eps == 'constraint':
			eps = 500.
		else:
			eps = eps/417.8
		bA, bB = e
		for a in bead_ref[bA]:
			for b in bead_ref[bB]:
				#
				print 'BOND %s %s\t%.3f\t%.3f' % (a, b, eps, l)
				 # F4 F4   500 3.500

def parse_angles(angle_dic, bead_ref):
	for e in angle_dic:
		angle, eps = angle_dic[e]
		eps = eps/4.178
		bA, bB, bC = e
		for a in bead_ref[bA]:
			for b in bead_ref[bB]:
				for c in bead_ref[bC]:
					print 'ANGLE %s %s %s\t%.2f\t%i' % (a,b,c,eps,angle)

def parse_dih(dih_dic, bead_ref):
	for e in dih_dic:
		e_type, angle, eps = dih_dic[e]
		eps = eps/417.8
		bA, bB, bC, bD = e
		for a in bead_ref[bA]:
			for b in bead_ref[bB]:
				for c in bead_ref[bC]:
					for d in bead_ref[bD]:
						print 'DIHEdral %s %s %s %s\t%.2f\t%i\t%i' % (a,b,c,d,eps,e_type, angle)

# DNA
parse_bonds(dna_bond_dic, dna_bead_ref)
parse_bonds(rna_bond_dic, rna_bead_ref)

parse_angles(dna_angle_dic, dna_bead_ref)
parse_angles(rna_angle_dic, rna_bead_ref)

parse_dih(dna_dih_dic, dna_bead_ref)
parse_dih(rna_dih_dic, rna_bead_ref)


