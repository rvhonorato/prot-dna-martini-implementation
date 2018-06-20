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

dih_dic = {
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

for e in dih_dic:
	e_type, angle, eps = dih_dic[e]
	eps = eps/417.8
	bA, bB, bC, bD = e
	for a in bead_ref[bA]:
		for b in bead_ref[bB]:
			for c in bead_ref[bC]:
				for d in bead_ref[bD]:
					print 'DIHEdral %s %s %s %s\t%.2f\t%i\t%i' % (a,b,c,d,eps,e_type, angle) 