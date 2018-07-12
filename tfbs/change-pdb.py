# change the pdb in a param file
import sys

paraml = open(sys.argv[1]).readlines()
target = open(sys.argv[2]).readlines()

for i, l in enumerate(paraml):
	if "chain = 'A'," in l:
		idxA = i
	if "chain = 'B'," in l:
		idxB = i

paraml[idxA+1] = '      pdbdata = %s,\n' % repr(''.join(target)[:-1])
paraml[idxB+1] = '      pdbdata = %s,\n' % repr(''.join(target)[:-1])

open(sys.argv[1],'w').write(''.join(paraml))
