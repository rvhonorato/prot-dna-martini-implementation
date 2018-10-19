# based on the submission, find which model belong to which run
import glob, os

# create pdb list
pdb_l = []
for pdb in glob.glob('/home/rodrigo/nucleosome/capri/runs/*pdb.gz'):
    pdb_l.append(pdb)

pdb_dic = {}
for pdb in glob.glob('/home/rodrigo/nucleosome/capri/*pdb'):
    pdb_dic[pdb] = {}
    for complex in pdb_l:
        cmd = 'refe %s\nmobi %s\nATOMS CA\nALIGN\nFIT\nquit' % (pdb, complex)
        output = os.popen('echo "%s" | profit' % cmd)  # if this fails, check the terminal atoms..
        result = [l for l in output if 'RMS:' in l][0]
        rms = float(result.split()[-1])
        pdb_dic[pdb][complex] = rms

out = open('found.csv','w')
for pdb in pdb_dic:
    min_rms = min(pdb_dic[pdb].values())
    for name, rms in pdb_dic[pdb].items():
        if rms == min_rms:
            id = name.split('/')[-1].split('complex')[0]
            out.write("%s,%.4f,%s,%s\n" % (pdb, rms, id, name))

out.close()