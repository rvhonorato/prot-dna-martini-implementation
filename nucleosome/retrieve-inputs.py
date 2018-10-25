# go into the capri directory and retrieve relevant information
import glob, os

os.chdir('/home/rodrigo/nucleosome/capri/cg-runs')

capri_run_dir = '/data/capri/Capri31/Target95/runs'

runs = [p for p in glob.glob('%s/*' % capri_run_dir) if not '.' in p]

for run in runs:

    identifier = run.split('/')[-1]

    if not os.path.isdir(identifier):
        os.system('mkdir %s' % identifier)

    # # pdbs
    # for p in glob.glob('%s/data/ensemble-models/*pdb' % run):
    #     os.system('cp %s %s/' % (p, identifier))
    #
    # os.system('cp %s/data/sequence/protein2.pdb %s/' % (run, identifier))
    #
    # restraints
    os.system('cp %s/data/distances/* %s' % (run, identifier))

    # params
    os.system('cp %s/*web %s' % (run, identifier))

    # run.cns
    os.system('cp %s/run.cns %s/run.cns.ori' % (run, identifier))
