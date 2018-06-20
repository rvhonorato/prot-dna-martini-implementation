# calculate success rate in diff thresholds
import glob, os

ls = [f for f in glob.glob('*') if not '.' in f]


topL = [1,5,10,50,100]
# topL = [1,4,10,50,100,200]
# topL = [1,4,10,50,100,200,1000]
# runL = ['run1','run2']
runL = ['run1']
phaseL = ['water']

for run in runL:
	print run
	for phase in phaseL:
		print phase
		for top in topL:
			high_counter = .0
			medium_counter = .0
			acceptable_counter = .0
			#
			total_counter = .0
			#
			for f in ls:
				data_f = '%s/%s/%s.dat' % (f, run, phase)
				# for l in open()
				if os.path.isfile(data_f):
					total_counter += 1
					#
					irmsd_list = [float(e.split('\t')[6]) for e in open(data_f).readlines()[1:top+1]]
					#
					if any([v <= 4.0 for v in irmsd_list]):
						acceptable_counter += 1
					if any([v <= 2.0 for v in irmsd_list]):
						medium_counter += 1
					if any([v <= 1.0 for v in irmsd_list]):
						high_counter += 1

			#
			acceptable_success_rate = acceptable_counter/total_counter
			medium_success_rate = medium_counter/total_counter
			high_success_rate = high_counter/total_counter
			print '%i\t%.2f\t%.2f\t%.2f' % (top, acceptable_success_rate, medium_success_rate, high_success_rate)




