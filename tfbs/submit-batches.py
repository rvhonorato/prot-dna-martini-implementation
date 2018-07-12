#
# This will be a huge job and PROCESSING stage is sequential, which means 
#  that if all 4096 complexes are submitted at once the next user will need 
# to wait for all of it to be finished.
#
#  To avoid this, submit the complexes in batches of 100
#
import os, sys, glob, subprocess, time

def chunks(l, n):
	#
	# shamelesly copied from https://stackoverflow.com/a/312464
	#
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def run(cmd, outputf):
	with open("./%s" % outputf, "w") as f:
		process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
		process.wait()

def run2(cmd, outputf):
	with open("./%s" % outputf, "w") as f:
		process = subprocess.Popen(cmd.split(), shell=False, stderr=f)
		process.wait()

#--------#


# create batches
ls = [f for f in glob.glob('*') if not '.' in f]
ls.sort()

submission_batches = list(chunks(ls, 100))
print len(submission_batches)
# submission_batches = list(chunks(ls, 5))

for i, batch in enumerate(submission_batches):

	print '>>> Batch %i\n' % i
	#======================#
	# stage 1 - submission #
	#======================#
	for comp in batch:
		# get in there
		os.chdir(comp)
		# has it been submited?
		if not os.path.isfile('submission.log'):
			# no, submit
			cmd = 'python /home/rodrigo/Nostromo/scripts/run_haddock22_file.py %s haddockparam.web' % comp
			run(cmd, 'submission.log')
		# get out
		os.chdir('..')
	
	#======================#
	# stage 2 - check      #
	#======================#
	complete_check = False

	while not complete_check:

		for comp in batch:
			os.chdir(comp)
			# is it done?
			cmd = '/home/rodrigo/haddock-CSB-tools/server_related/check-haddockrun.csh submission.log'
			run(cmd, 'check.log')
			status = 'unknown'
			try:
				log = open('check.log').readlines()[0][:-1]
				status = log.split()[-1]
				print comp, status
			except:
				print 'there is something wrong with %s, checking it did not produce any output' % comp
			#
			if 'Finished' in log:
				# it finished and check-haddockrun.csh has downloaded it
				#  get the correct name
				try:
					runf = glob.glob('%s*.tgz' % comp)[0]
				except:
					print 'Something went wrong with downloading %s' % comp
					# exit()
				# uncompress it into the correct place if it has not been before
				if os.path.isfile(runf) and not os.path.isdir('run1'):
					cmd = 'tar zxf %s' % runf
					run2(cmd,'tar.log')
					# check if it uncompression was ok
					tar_check = open('tar.log').readlines()
					if tar_check:
						os.system('rm -rf %s' % runf)
					else:					
						os.system('mv %s run1' % runf.split('.')[0])
					
			os.chdir('..')
			# wait a few seconds to be sure we wont break anything
			time.sleep( 2 )


		# check
		check_l = [bool(glob.glob('%s/run1/run.cns' % c)) for c in batch]
		# print check_l, all(check_l)
		if all(check_l):
			# this means all of them have been properly parsed
			# exit()
			complete_check = True
		else:
			# wait some time
			# print 'sleeping'
			time.sleep( 60 )
		print '-' * 10
		#
		# debug exit
		#
		# exit()





