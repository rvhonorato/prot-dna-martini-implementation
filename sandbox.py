
import glob, os
ls = [f for f in glob.glob('*') if not '.' in f]


for f in ls:
	runf = '%s/run.sh' % f
	if os.path.isfile(runf):
		a = open(runf).readlines()[-1][-1]
		try:
			print int(a), f
		except:
			pass
	else:
		print f