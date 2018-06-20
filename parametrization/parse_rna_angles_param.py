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
'ASC2':['ARS1','RH1'],
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


angle_dic = {
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


for e in angle_dic:
	angle, eps = angle_dic[e]
	# l = l*10
	eps = eps/4.178
	bA, bB, bC = e
	for a in bead_ref[bA]:
		for b in bead_ref[bB]:
			for c in bead_ref[bC]:
				print 'ANGLE %s %s %s\t%.2f\t%i' % (a,b,c,eps,angle)

