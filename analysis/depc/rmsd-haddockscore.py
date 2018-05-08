# pdb, rmsd, haddockscore

haddock_score_dic = dict([e.split() for e in open('file.nam_haddock-score').readlines()[1:]])
rmsd_dic = dict([e.split() for e in open('file.nam_rmsd').readlines()[1:] if e.split()])

outA = open('melqui-inputA.csv','w')
outB = open('melqui-inputB.csv','w')
for pdb in haddock_score_dic:
	haddock_score = float(haddock_score_dic[pdb])
	rmsd = float(rmsd_dic[pdb])
	#
	outA.write('%.3f %.3f\n' % (rmsd, haddock_score))
	outB.write('%s\n' % pdb)

outA.close()
outB.close()

