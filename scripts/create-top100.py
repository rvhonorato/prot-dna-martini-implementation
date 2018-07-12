# create top 100 for submission

f = open('run1/structures/it1/water/file.nam').readlines()

top100 = []
for p in f[:100]:
	pdbf = [l for l in open('run1/structures/it1/water/%s' % p[:-1]).readlines() if 'ATOM' in l[:4]]
	top100.append(pdbf)

out = open('dbg','w')
for i, pdb in enumerate(top100):
	ter_l 
	out.write('MODEL %i\n%s\nENDMDL\n' % (i+1, ''.join(pdb)[:-1]))

out.close()

