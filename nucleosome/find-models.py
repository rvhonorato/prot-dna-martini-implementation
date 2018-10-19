# based on the submission, find which model belong to which run

import glob, os

pdb_l = []

run_path_l = ['/data/capri/Capri31/Target95/runs/T95-all-passive-fcc',
    '/data/capri/Capri31/Target95/runs/T95-ambig-fullbases',
    '/data/capri/Capri31/Target95/runs/T95-cm-Cys-Lys',
    '/data/capri/Capri31/Target95/runs/T95-DNA-only-fcc',
    '/data/capri/Capri31/Target95/runs/T95-server-fcc',
    '/data/capri/Capri31/Target95/runs/T95-server-rmsd']

# out = open('/home/rodrigo/pdb.list','w')
for path in run_path_l:
    for pdb in glob.glob('%s/structures/it1/water/*pdb*' % path):
        name = path.split('/')[-1] + '-' + pdb.split('/')[-1]
        os.system('cp %s /home/rodrigo/nucleossome/capri/runs/%s' % (pdb, name))
        # pdb_l.append(pdb)
        # out.write(pdb+'\n')

# out.close()


# capri_models = glob.glob('/home/rodrigo/nucleossome/capri/target95*pdb')

# print pdb_l[0], capri_models[0]

