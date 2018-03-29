bead_ref = {'BB1': ['NB1'],	
'BB2': ['NB2'],	
'BB3': ['NB3'],	

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
'TSC3': ['TNS2', 'NH6']}


angle_dic = {
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


for e in angle_dic:
	angle, eps = angle_dic[e]
	# l = l*10
	eps = eps/4.178
	bA, bB, bC = e
	for a in bead_ref[bA]:
		for b in bead_ref[bB]:
			for c in bead_ref[bC]:
				print 'ANGLE %s %s %s\t%.2f\t%i' % (a,b,c,eps,angle)
	










