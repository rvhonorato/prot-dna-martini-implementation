# martinize!

# read the tbl file

f = 'air_trueiface_unbound.tbl'

bb_d ={"BB1": ["P", "O1P", "O2P", "O5'", "OP1", "OP2"],
"BB2": ["C5'", "O4'", "C4'"],
"BB3": ["C3'", "C2'", "C1'"]}

sc_d = {"SC1": ["N9", "C4", "N1", "C6"],
"SC2": ["O2", "C2", "N2", "N3"],
"SC3": ['C7','N6','O6', 'N1','O4','N4','C6','C5','C4'],
"SC4": ["C8", "N7", "C5"]}

out = open('air_trueiface_unbound-cg.tbl','w')

for l in open(f).readlines():
	atoms = ''.join(''.join(l.split('name')[1:]).split('))')[0].split('or')).split()
	bb = list(set([b for b in bb_d for e in atoms for c in bb_d[b] if e == c]))
	bb.sort()
	sc = list(set([s for s in sc_d for e in atoms for c in sc_d[s] if e == c]))
	sc.sort()
	if sc:
		n_l = l.split('name')[0] + 'name ' + ' or name '.join(sc) + '))\n'
	elif bb:
		n_l = l.split('name')[0] + 'name ' + ' or name '.join(bb) + '))\n'
	else:
		n_l = l
	#
	out.write(n_l)
out.close()


	