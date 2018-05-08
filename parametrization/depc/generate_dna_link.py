# create link file for all bases

nuc_bases = ['DA','DC','DG','DT','hDA','hDC','hDG','hDT']

out = open('dna-cg.link','w')

for a in nuc_bases:
	for b in nuc_bases:
		# print a, b
		out.write('link nuc head - %s tail + %s end\n' %(a, b))
	out.write('\n')

out.close()