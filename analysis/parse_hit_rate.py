# calculate success rate in diff thresholds
import glob, os

ls = [f for f in glob.glob('*') if not '.' in f]

topL = [1,5,10,50,100]
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
			acceptable_hit_rate_l = []
			medium_hit_rate_l = []
			high_hit_rate_l = []
			for f in ls:
				data_f = '%s/%s/%s.dat' % (f, run, phase)
				# for l in open()
				if os.path.isfile(data_f):
					total_counter += 1
					#
					irmsd_list = [float(e.split('\t')[6]) for e in open(data_f).readlines()[1:top+1]]
					#
					[acceptable_hit_rate_l.append(v) for v in irmsd_list if v <= 4.0]
					[medium_hit_rate_l.append(v) for v in irmsd_list if v <= 2.0]
					[high_hit_rate_l.append(v) for v in irmsd_list if v <= 1.0]
			#
			acceptable_hit_rate = len(acceptable_hit_rate_l) / (total_counter*top)
			medium_hit_rate = len(medium_hit_rate_l) / (total_counter*top)
			high_hit_rate = len(high_hit_rate_l) / (total_counter*top)
			print '%s,%i,%.2f,%.2f,%.2f' % (run, top, acceptable_hit_rate, medium_hit_rate, high_hit_rate)
			# exit()





