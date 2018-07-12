# create a table with all irmsd from all phases
import glob
import pandas as pd


def read_data(input_f, name, run):
	for i, e in enumerate(open(input_f).readlines()[1:]):
		data = e.split()
		#
		rank = int(data[2])
		irmsd = float(data[6])
		# pdb = data[2]
		phase = data[0]
		#
		# irmsd_dic['pdb'].append(pdb)
		irmsd_dic['rank'].append(rank)
		irmsd_dic['irmsd'].append(irmsd)
		irmsd_dic['name'].append(name)
		irmsd_dic['phase'].append(phase)
		irmsd_dic['run'].append(run)

###

global irmsd_dic

ls = [f for f in glob.glob('*') if not '.' in f]

irmsd_dic = {'rank':[],'irmsd':[], 'name': [], 'phase': [], 'run': []}


runL = ['run1', 'run2']#, 'run3','run4']

irmsd_dic_it0 = {}
irmsd_dic_it1 = {}
irmsd_dic_water = {}

for f in ls:
	irmsd_dic_it0[f] = []
	irmsd_dic_it1[f] = []
	irmsd_dic_water[f] = []
	for run in runL:
		it0_f = '%s/%s/it0.dat' % (f, run)
		it1_f = '%s/%s/it1.dat' % (f, run)
		water_f = '%s/%s/water.dat' % (f, run)

		irmsd_dic_it0[f] = [float(e.split('\t')[6]) for e in open(it0_f).readlines()[1:]]
		irmsd_dic_it1[f] = [float(e.split('\t')[6]) for e in open(it1_f).readlines()[1:]]
		irmsd_dic_water[f] = [float(e.split('\t')[6]) for e in open(water_f).readlines()[1:]]

		pd.DataFrame(irmsd_dic_it0).to_csv('%s_it0-irmsd.csv' % run)
		pd.DataFrame(irmsd_dic_it1).to_csv('%s_it1-irmsd.csv' % run)
		pd.DataFrame(irmsd_dic_water).to_csv('%s_water-irmsd.csv' % run)

		read_data(it0_f, f, run)
		read_data(it1_f, f, run)
		read_data(water_f, f, run)
			
df = pd.DataFrame.from_dict(irmsd_dic)
df.to_csv('-benchmark.csv')

