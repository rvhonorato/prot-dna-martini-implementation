# prepare dimers for scoring
import glob
import subprocess

target_list = ['1A74', '1AZP', '1JJ4', '1ZME']

for d in target_list:
    pdb_list = glob.glob(f'{d}/structures/*pdb')
    for pdb in pdb_list:
        p = subprocess.Popen(['/home/abonvin/haddock2.4/tools/pdb_chain-segid', pdb], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        new_pdb = p.communicate()
        out = open(pdb,'w')
        out.write(new_pdb[0].decode('utf-8'))
        out.close()

    # split in batches of 100
    batch_list =  [pdb_list[i:i+100] for i in range(0, len(pdb_list), 100)]

    for i, batch in enumerate(batch_list):
        f_out = open(f'{d}/structures/filelist{i+1}.list', 'w')
        for e in batch:
            f_out.write(f'{e}\n')
        f_out.close()

    # edit scoring.inp