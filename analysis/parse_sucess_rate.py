# calculate success rate in diff thresholds
import glob, os, argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument("runn", type=int,
                    help="Run number")

# parser.add_argument("phase", type=str,
#                     help="which phase to analyze")

args = parser.parse_args()

run = 'run%i' % args.runn

# if args.phase not in ['water','it1', 'it0']:
# 	print '> Please provide a valid phase'
# 	exit()

ls = [f for f in glob.glob('*') if not '.' in f]

topL = [1, 5, 10, 50, 100, 400, 1000]

# print args.phase
print 'top acceptable medium high'
issue_l = []
r_dic = {}
for phase in ['water','it1', 'it0']:
	print phase
	for top in topL:
		#
		r_dic[top] = {}
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
			else:
				issue_l.append(f)

		#
		acceptable_success_rate = (acceptable_counter/total_counter) * 100
		medium_success_rate = (medium_counter/total_counter) * 100
		high_success_rate = (high_counter/total_counter) * 100
		# print '%i %.2f %.2f %.2f' % (top, acceptable_success_rate, medium_success_rate, high_success_rate)
		#
		r_dic[top]['acceptable'] = acceptable_success_rate
		r_dic[top]['medium'] = medium_success_rate
		r_dic[top]['high'] = high_success_rate

	print 'n=%i'% int(total_counter)
	issues_l = list(set(issue_l))
	issues_l.sort()
	print 'issues=%s' % ' '.join(issues_l)

	if len(issues_l) == 0:
		df = pd.DataFrame.from_dict(r_dic)
		df.to_csv('run%i_%s_success_rate.csv' % (args.runn, phase))
		print df


