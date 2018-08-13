import glob


ls = glob.glob('*')

print 'seq,name,haddock_score,bsa,desolv,totale,bonds,angles,improper,dihe,vdw,elec,air,cdih,coup,rdcs,vean,dani,xpcs,rg'
for seq in ls:
	mls = glob.glob('%s/run1/cluster*' % seq)
	for pdb in mls:
		# pdb = 'cluster1_1.pdb'
		data = open(pdb).readlines()
		energies_l = map(float, data[7].split(':')[-1].split(','))
		totale, bonds, angles, improper, dihe, vdw, elec, air, cdih, coup, rdcs, vean, dani, xpcs, rg = energies_l
		bsa = float(data[28].split(':')[-1])
		binding = float(data[26].split(':')[-1])
		desolv = float(data[23].split(':')[-1])
		haddock_score = (1.0 * vdw) + (0.2 * elec) + (0.0 * desolv) + (0.1 + air)
		print '%s,%s,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f' % (seq, pdb, haddock_score, bsa, desolv, totale, bonds, angles, improper, dihe, vdw, elec, air, cdih, coup, rdcs, vean, dani, xpcs, rg)