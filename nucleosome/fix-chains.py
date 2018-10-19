# make submission chains match runs
import glob, os, subprocess

def run(cmd, outputf):
    with open(outputf, "w") as f:
        process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
        process.wait()

exe = 'python /home/rodrigo/pdb-tools/pdb_rplchain.py'
wd = os.chdir('/home/rodrigo/lab/nucleosome/capri')

A = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
B = ['K', 'L', 'M']

pdb_l = glob.glob('target95*pdb')
print 'what'
for pdb in pdb_l:
    for chain in A:
        cmd = '%s -%s -X %s' % (exe, chain, pdb)
        run(cmd, 'oo')
        os.system('mv oo %s' % pdb)
    for chain in B:
        cmd = '%s -%s -Y %s' % (exe, chain, pdb)
        run(cmd, 'oo')
        os.system('mv oo %s' % pdb)
    #
    cmd = '%s -X -A %s' % (exe, pdb)
    run(cmd, 'oo')
    os.system('mv oo %s' % pdb)

    cmd = '%s -Y -B %s' % (exe, pdb)
    run(cmd, 'oo')
    os.system('mv oo %s' % pdb)

    exit()