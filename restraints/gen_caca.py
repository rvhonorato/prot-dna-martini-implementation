# read a file and output
import sys
print ''.join(['%s\n' % ' '.join(j) for j in [('assign ( name CA and segid', e[1], 'and resi', e[0],') ( name CA and segid', e[4], 'and resi', e[3], ')', e[6],' 0.5000 0.5000') for e in [a.split() for a in [l for l in open(sys.argv[1]).readlines() if l.split()[2] == 'CA' and l.split()[5] == 'CA']]]])

#for l in open(sys.argv[1]).readlines():
#    resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
#    if atomA == 'CA' and atomB == 'CA':
#    	print 'assign (name CA and segid %s and resi %s) (name CA and segid %s and resi %s) %.4f 0.500 0.500' % (chainA, resA, chainB, resB, float(dist))
