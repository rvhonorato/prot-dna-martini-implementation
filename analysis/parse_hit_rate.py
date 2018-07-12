# calculate success rate in diff thresholds
import glob, os, argparse
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument("runn", type=int,
                    help="Run number")

parser.add_argument("phase", type=str,
                    help="which phase to analyze")

args = parser.parse_args()

run = 'run%i' % args.runn

ls = [f for f in glob.glob('*') if not '.' in f]

topL = [1, 5, 10, 50, 100, 400, 10000]

print args.phase
print 'top acceptable medium high'
issue_l = []
r_dic = {}

for top in topL:

	r_dic[top] = {}

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
		data_f = '%s/%s/%s.dat' % (f, run, args.phase)
		# for l in open()
		if os.path.isfile(data_f):
			total_counter += 1
			#
			irmsd_list = [float(e.split('\t')[6]) for e in open(data_f).readlines()[1:top+1]]
			#
			[acceptable_hit_rate_l.append(v) for v in irmsd_list if v <= 4.0]
			[medium_hit_rate_l.append(v) for v in irmsd_list if v <= 2.0]
			[high_hit_rate_l.append(v) for v in irmsd_list if v <= 1.0]
		else:
			issue_l.append(f)
	#
	acceptable_hit_rate = (len(acceptable_hit_rate_l) / (total_counter*top)) * 100
	medium_hit_rate = (len(medium_hit_rate_l) / (total_counter*top)) * 100
	high_hit_rate = (len(high_hit_rate_l) / (total_counter*top)) * 100

	r_dic[top]['acceptable'] = acceptable_hit_rate
	r_dic[top]['medium'] = medium_hit_rate
	r_dic[top]['high'] = high_hit_rate

	print '%s %i %.2f %.2f %.2f' % (run, top, acceptable_hit_rate, medium_hit_rate, high_hit_rate)
			# exit()


print 'n=%i'% int(total_counter)
issues_l = list(set(issue_l))
issues_l.sort()
print 'issues=%s' % ' '.join(issues_l)

if len(issues_l) == 0:
	df = pd.DataFrame.from_dict(r_dic)
	df.to_csv('run%i_%s_hit_rate.csv' % (args.runn, args.phase))


