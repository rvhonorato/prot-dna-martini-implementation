# from the reference structure

# 1. filter accessible residues in protein and dna nacess < 30%
dna_access = 'dna.rsa'
protein_access = '5uan_A.rsa'

# dna_access_dic = dict([(int(l.split()[3]), float(l.split()[6])) for l in open(dna_access).readlines()[4:-5]])
protein_access_dic = dict([(int(l.split()[3]), float(l.split()[6])) for l in open(protein_access).readlines()[4:-4]])

dna_access_dic = {}
for l in open('dna.asa'):
	data = l.split()
	atom = data[2]
	resnum = int(data[5])
	asa = float(data[9])
	#
	try:
		_ = dna_access_dic[resnum]
	except:
		dna_access_dic[resnum] = {}
	#
	dna_access_dic[resnum][atom] = asa

# 3. get contacts, 4.0A
dnasc_atoml = ['N9','C4','C2','N3','C6','N6','N1','C8','N7','C5','N1','C6','N3','C2','O2','C5','C4','N4','O4','C7', 'C5M']
proteinbb_atoml = ['CA','C','N','O']

sc_protein_active_resl = []
bb_protein_active_resl = []

dna_sc_atomlist = []
dna_bb_atomlist = []
for l in open('5.con'):
	resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
	#
	resA = int(resA)
	resB = int(resB)
	#
	if atomB == 'OP2':
		atomB = 'O2P'
	if atomB == 'OP1':
		atomB = 'O1P'
	if atomB == 'C7':
		atomB = 'C5M'
	#
	if atomA not in proteinbb_atoml and atomB in dnasc_atoml:
		# pSC-dSC
		if protein_access_dic[resA] >= 30.0:
			# permit this protein AA
			sc_protein_active_resl.append(resA)
			# print 'sc', resA, atomA, atomB
			dna_sc_atomlist.append(atomB)
	if atomA not in proteinbb_atoml and atomB not in dnasc_atoml:
		# pSC-dBB
		if protein_access_dic[resA] >= 30.0:
			# permit this protein AA
			bb_protein_active_resl.append(resA)
			dna_bb_atomlist.append(atomB)
			# print 'bb', resA, atomA, atomB


sc_protein_active_resl = list(set(sc_protein_active_resl))
bb_protein_active_resl = list(set(bb_protein_active_resl))
sc_protein_active_resl.sort()
bb_protein_active_resl.sort()

dna_bb_atomlist = list(set(dna_bb_atomlist))
dna_sc_atomlist = list(set(dna_sc_atomlist))

print sc_protein_active_resl
print bb_protein_active_resl




# d for d in 

# dna_sc_atomlist = []

# d for d in 
out = open('dbg','w')
for r in sc_protein_active_resl:
	tbw = 'assign ( resid %i and segid A )\n       (\n' % r
	for e in [d for d in dna_access_dic if dna_access_dic[d] >= 30.0]:
		tbw += '        ( resid %i and segid B and ( name %s ))\n     or\n' %  (e, ' or name '.join(dna_sc_atomlist))
	out.write(tbw[:-3] + ')  2.0 2.0 0.0\n\n')
# out.close()
	# exit()

for r in bb_protein_active_resl:
	if r not in sc_protein_active_resl:
		tbw = 'assign ( resid %i and segid A )\n       (\n' % r
		for e in [d for d in dna_access_dic if dna_access_dic[d] >= 30.0]:
			tbw += '        ( resid %i and segid B and ( name %s ))\n     or\n' %  (e, ' or name '.join(dna_bb_atomlist))
		out.write(tbw[:-3] + ')  2.0 2.0 0.0\n\n')
out.close()


# # 

# l.split('name')[0] + 'name ' + ' or name '.join(sc) + '))\n'
# l.split('name')[0] + 'name ' + ' or name '.join(sc) + '))\n'

# assign ( resid 15 and segid A)
#        (
#         ( resid 1 and segid C and (name C1' or name O4' or name C4' or name C3' or name C2' or name O3' or name C5' or name O5' or name P or name O1P or name O2P or name H5' or name H5'' or name H4' or name H3' or name H2' or name H2'' or name H1'))
#        )  2.0 2.0 0.0



# assign ( resid 32 and segid A)
#        (
#         ( resid 24 and segid C)
#      or
#         ( resid 25 and segid C and (name H1 or name H21 or name H22 or name N3 or name N7 or name O6 or name C2 or name C4 or name C5 or name C6 or name C8))
#      or
#         ( resid 23 and segid C and (name C1' or name O4' or name C4' or name C3' or name C2' or name O3' or name C5' or name O5' or name P or name O1P or name O2P or name H5' or name H5'' or name H4' or name H3' or name H2' or name H2'' or name H1'))
#        )  2.0 2.0 0.0










# ( resid 25 and segid C and (name H1 or name H21 or name H22 or name N3 or name N7 or name O6 or name C2 or name C4 or name C5 or name C6 or name C8))






# 2. define two classes of interaction, pSC-dSC, pSC-dBB