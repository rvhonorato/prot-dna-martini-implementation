import glob
import os

ls = glob.glob('*/')

data_dic = {}
for f in ls:
    pdbname = f.split('/')[0]
    dataf = '%srun1/it0.dat' % f
    if os.path.isfile(dataf):
        data_dic[pdbname] = {}
        for l in open(dataf).readlines()[1:]:
            data = l.split('\t')
            #
            structure = data[1]
            rank = int(data[2])
            irms = float(data[6])
            #
            data_dic[pdbname][structure] = (rank, irms)

# how many acceptable models are there in top200?
# target_rank = 200
target_rank = 25
for pdb in data_dic:
    counter = 0
    total_acceptable = len([data_dic[pdb][e][1] for e in data_dic[pdb] if data_dic[pdb][e][1] <= 4.0])
    for structure in data_dic[pdb]:
        rank, irms = data_dic[pdb][structure]
        #
        if irms <= 4.0 and rank <= target_rank:
            counter += 1
    #
    if total_acceptable > target_rank and counter < target_rank:
        print pdb, total_acceptable, counter

# for pdb in data_dic:
# acceptable = len([v for v in data_dic[pdb].values() if v <= 4.0])
# print pdb, acceptable
