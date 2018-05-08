

import os, subprocess, glob

def run(cmd, outputf):
	with open("./%s" % outputf, "w") as f:
		process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
		process.wait()

benchmark_l = [e for e in glob.glob('*') if not 'txt' in e]

for target in benchmark_l:
	print target
	os.chdir(target)
	os.chdir('run1')
	cmd = 'python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py'
	# print cmd
	run(cmd, 'haddock.out')
	os.chdir('..')
	os.chdir('..')
	# exit()
