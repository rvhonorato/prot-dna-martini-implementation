# create a histogram of number of residues
import glob,sys
import numpy as np
#import matplotlib.pyplot as plt

resl = []
for pdb in open('pdb.list'):
	resl.append(len([l for l in open(pdb.split('\n')[0]) if 'CA' in l]))

x = np.array(resl)
a,b = np.histogram(x)
for i, e in enumerate(a):
	print b[i+1], e

#fig = plt.figure()
#plt.hist(x, bins='auto')
#plt.title("CA distribution in pdb.list")
#fig.savefig('~/CA-dist.png')
