# edit cutnb and ctofnb in protocol/read_struct.cns to see if there's any speedup
import glob, os, subprocess


def run(cmd, outputf):
	with open(outputf, "w") as f:
		process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
		process.wait()

# ls = glob.glob('*')
start = 8
end = 20

# for f in ls:
	# os.chdir(f)
dna_chain = open('run.sh').readlines()[-1][-1]
for i, e in enumerate(range(start, end,1)):
	n_cutnb = e
	n_ctofnb = e-1
	n_ctonnb = e-2
	runn = i+1
	# renumber run number in new.html
	new_f = open('new.html').readlines()
	out = open('new.html.%i' % runn,'w')
	for l in new_f:
		if 'RUN_NUMBER' in l:
			l = 'RUN_NUMBER=%i<BR>\n' % runn
		out.write(l)
	out.close()
	#
	os.system('cp new.html.%i new.html' % runn)
# 	#
	cmd = 'python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py'
	run(cmd, 'haddock.log')
	#
	cmd = 'bash /home/rodrigo/Nostromo/scripts/run_threshold.sh %s %i %i %i %i' % (dna_chain, runn, n_cutnb, n_ctofnb, n_ctonnb)
	run(cmd, 'log')

# 	open('run-opt-%i.sh' % i,'w').write('''python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py
# bash /home/rodrigo/Nostromo/scripts/run_threshold.sh %s %i %i %i ''' % (dna_chain, runn, n_cutnb, n_ctofnb)

