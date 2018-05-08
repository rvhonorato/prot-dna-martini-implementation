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

dih_dic = {
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



for e in dih_dic:
	e_type, angle, eps = dih_dic[e]
	eps = eps/417.8
	bA, bB, bC, bD = e
	for a in bead_ref[bA]:
		for b in bead_ref[bB]:
			for c in bead_ref[bC]:
				for d in bead_ref[bD]:
					print 'DIHEdral %s %s %s %s\t%.2f\t%i\t%i' % (a,b,c,d,eps,e_type, angle) 


