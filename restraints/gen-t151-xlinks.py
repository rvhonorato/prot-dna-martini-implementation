def find_key(dic, val):
	'''return the key of dictionary dic given the value'''
	return [k for k, v in dic.iteritems() if v == val][0]

xlink_l = [(339,343),(371,385),(526,549),(371,384),(989,989),(526,343),(371,363),
	(966,343),(371,385),(762,343),(371,384),(959,549),(339,854),(1040,881),(526,753),
	(854,343),(526,482),(487,231),(1127,231),(358,364),(989,343),(1235,343),(343,959),
	(989,549),(1188,231),(966,549),(989,363),(370,384),(339,231),(636,482),(358,364),
	(941,549),(989,854),(343,959),(545,231),(526,959),(937,762),(989,762),(526,231),
	(1040,865),(371,364),(937,343),(966,231),(339,526),(937,549),(937,959),(966,231),
	(410,343),(545,959),(231,959),(1040,231),(410,231),(98,168),(1127,1127),(487,487),
	(1235,1188),(339,959),(989,343),(487,989),(371,363),(937,231),(937,753),(1040,343),
	(1127,549),(1235,231),(168,98),(410,385),(1040,989),(941,231),(941,339),(941,854),
	(1127,989),(1188,989),(1184,881),(339,989),(1235,231),(989,385),(358,989),(989,959),
	(893,1040),(1227,348),(1235,358),(893,865),(1227,168),(1227,1227),(989,881),(526,343),
	(1235,343),(1184,989),(762,959),(1198,231),(966,339),(1235,364),(854,959),(941,231),
	(1184,231),(1235,168),(487,636),(1184,343),(1227,1188),(487,636),(168,371),(784,410),
	(1040,854),(1225,1188),(1267,1127),(168,358),(358,854),(487,526),(941,343),(865,881),
	(1184,1184),(1188,1188),(1235,1235),(941,343),(487,545),(410,487),(410,881),(784,989),
	(98,1188),(1227,989),(168,1188),(1227,231),(941,854),(545,545),(1184,1127),(482,636),
	(937,989),(941,989)]

xlink_dic = {}
for e in xlink_l:
	try:
		xlink_dic[e[0]].append(e[1])
	except:
		xlink_dic[e[0]] = [e[1]]


# find which res belongs to each chain
# chain_dic = dict([(e[22:26], []) for e in open('complex_7w.pdb').readlines() if 'ATOM' in e[:4]])

chain_dic = {}
for l in open('complex_7w.pdb').readlines():
	if 'ATOM' in l[:4]:
		chain = l[21]
		resnum = int(l[22:26])
		chain_dic[resnum] = chain


for r in xlink_dic:
	pairs = list(set(xlink_dic[r]))
	try:
		chainA = chain_dic[r]
	except:
		continue
	# tbw = 'assign 
	root = '(segid %s and resi %i and name CB)' % (chainA, r)
	tbw_l = []
	for i, p in enumerate(pairs):
		try:
			chainB = chain_dic[p]
		except:
			continue
		if chainA == chainB:
			continue
		###
		tbw_l.append('%s (segid %s and resid %i and name CB)' % (root, chainB, p))
	if tbw_l:
		print 'assign ' + tbw_l[0] + ' 20.0 10.0 0.0\n or ' + '\n or '.join(tbw_l[1:])
	# exit()
# assi (segid A and resid 10 and name CB) (segid B and resid 200 and name CB) 20.0 10.0 0.0


		# if i != len(pairs)-1:
		# 	tbw += '(name CB and segid %s and resi %i) or ' % (chainB, p)
		# else:
		# 	tbw += '(name CB and segid %s and resi %i) ' % (chainB, p)
	# tbw += ') 20.0 10.0 0.0'
	
	# print tbw

# (name CB and segid A and resi 545)


# ! HADDOCK AIR restraints for 1st selection
# !
# assign ( resid 1  and segid A)  ( ( resid 2  and segid B)  or  ( resid 3  and segid B) )  2.0 2.0 0.0


# ! HADDOCK AIR restraints for 2nd selection
# !
# assign ( resid 2  and segid B) ( ( resid 1  and segid A) )  2.0 2.0 0.0

# assign ( resid 3  and segid B)
#        (
#         ( resid 1  and segid A)
#        )  2.0 2.0 0.0