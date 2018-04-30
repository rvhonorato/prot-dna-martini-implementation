import glob

f_l = glob.glob('*')

for f in f_l:
	print f

f = '1W0T'
glob.glob('%s/*unbound*pdb' % f)

# check for multiple copies