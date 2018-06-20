import glob, os, subprocess

def run(cmd, outputf):
	with open("./%s" % outputf, "w") as f:
		process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
		process.wait()


######

for f in [f for f in glob.glob('*') if not '.' in f]:

	# create next dir
	if not os.path.isdir('%s/run3' % f):
		os.system('mkdir %s/run3' % f)

	if not os.path.isfile('%s/run3/haddockparam.web' % f):

		# setup new haddockparam.web
		prev_paramf = '%s/run2/haddockparam.web' % f
		if os.path.isfile(prev_paramf):
			os.system('cp %s %s/run3' % (prev_paramf, f))
		else:
			# run2 not found, this has failed before.
			print 'run2 not found for %s' % f
			continue
	
		paraml = open('%s/run3/haddockparam.web' % f).readlines()
		ambigl = open('%s/air_trueiface_unbound.tbl' % f).readlines()
		
		np = []
		air_check = 0
		for i, l in enumerate(paraml):
			
			# v2 specific settings

			# double check restraints
			if 'unambigtbldata' in l: # this should not exist
				nl = '  tbldata = %s,\n' % repr(''.join(ambigl))
				air_check += 1
			elif 'tbldata' in l: # 	this should exist
				# for this benchmark there is no case of unambigtbldata and tbldata on the same run.cns
				nl = '  tbldata = %s,\n' % repr(''.join(ambigl))

			# "Changing the dieletric constant to 78 would mimic the polarsability of water as a medium"
			elif 'epsilon' in l:
				nl = '  epsilon = 78.0,\n'
			elif 'runname' in l:
				nl = "  runname = '%s_e78',\n" % f
			else:
				nl = l
			
			# identify where desolv weight is
			if 'w_desolv' in l:
				desol_idx = i

			np.append(nl)
		
		# write	
		open('%s/run3/haddockparam.web' % f,'w').write(''.join(np))
		
		# re-open and edit weights
		nparaml = open('%s/run3/haddockparam.web' % f).readlines()
		nparaml[desol_idx+1] = '    0.0,\n'
		nparaml[desol_idx+2] = '    0.0,\n'
		nparaml[desol_idx+3] = '    0.0,\n'

		# done
		open('%s/run3/haddockparam.web' % f,'w').write(''.join(nparaml))

	# prepare for submission
	submissionf = '%s/run3/submission.log' % f
	if not os.path.isfile(submissionf):
		# not submitted yet
		cmd = 'python /home/rodrigo/Nostromo/run_haddock22_file.py %s_e78 %s/run3/haddockparam.web' % (f, f)
		# run(cmd, submissionf)

	else:
		# submitted
		if not os.path.isfile('%s/run3/run.cns' % f):
			# not uncompressed yet

			# check status/download if finished
			cmd = '/home/rodrigo/haddock-CSB-tools/server_related/check-haddockrun.csh %s' % submissionf
			run(cmd, 'check.log')
			status = 'unknown'
			try:
				log = open('check.log').readlines()[0][:-1]
				status = log.split()[-1]
			except:
				print 'there is something wrong with %s, check it' % f

			if 'Finished' in log:
				# it has been downloaded
				runf = glob.glob('%s_e78*.tgz' % f)[0]
				if os.path.isfile(runf):
					print 'Uncompressing %s' % runf
					os.system('mv %s %s' % (runf, f))
					os.chdir(f)
					os.system('tar zxf %s' % runf)
					os.system('mv %s/* run3/' % runf.split('.')[0])
					os.chdir('..')
				else:
					print 'Something went wrong with downloading %s' % f
					exit()
	# done