
chain_list = list(set([l[21] for l in open('ensemble_1.pdb').readlines() if 'ATOM' in l [:4]]))
chain_list.sort()

interface_res_dic = dict([(c, {}) for c in chain_list])
# interface_res_dic = {}
# for c in chain_list:
#     t_d = {}
#     for e in chain_list:
#         t_d[e] = []
#     interface_res_dic[c] = t_d
        # interface_res_dic[c] = {e: []}

# for l in open('ensemble_1_3.0.contacts'):
for l in open('ensemble_1_10.0.contacts'):
    resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
    #
    resA = int(resA)
    resB = int(resB)
    #
    #
    try:
        interface_res_dic[chainA][resA].append(chainB)
    except:
        interface_res_dic[chainA][resA] = []
        interface_res_dic[chainA][resA].append(chainB)
    #
    try:
        interface_res_dic[chainB][resB].append(chainA)
        # interface_res_dic[chainA][resA].append(chainB)
    except:
        interface_res_dic[chainB][resB] = []
        interface_res_dic[chainB][resB].append(chainA)


# out = open('active.list','w')
# for chain in active_res_dic:
#     # print chain, unbound_active_res_dic[chain]
#     out.write('sele %s, chain %s and resid %s\n' % (chain, chain, '+'.join(map(str, active_res_dic[chain]))))
# out.close()

out = open('ambig-new-10.tbl','w')
for chainA in interface_res_dic:
    # print interface_res_dic[chainA]
    for resA in interface_res_dic[chainA].keys():
        tbwA = 'resid %i and segid %s' % (resA, chainA)
        tbwB = []
        for chainB in list(set(interface_res_dic[chainA][resA])):
            active_reslist = interface_res_dic[chainB].keys()
            for resB in active_reslist:
                for candidate_chain in list(set(interface_res_dic[chainB][resB])):
                    if candidate_chain == chainA:
                        tbwB.append('( resid %i and segid %s )' % (resB, chainB))
                        # print resA, chainA, resB, chainB
        out.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
out.close()



    #     print resA, list(set(interface_res_dic[chainA][resA]))
    # print '#' * 10



# clean it
n_d = {}
for e in interface_res_dic:
    n_d[e] = {}
    for c in interface_res_dic[e]:
        if len(interface_res_dic[e][c]) != 0:
            n_d[e][c] = list(set(interface_res_dic[e][c]))


for chainA in interface_res_dic:
    for chainB in interface_res_dic[chainA]:




for chainA in interface_res_dic:
    for chainB in interface_res_dic[chainA]:
        tbwA = 'resid %i and segid %s' % (rA, a)
        tbwB = []
        for b in interface_res_dic[a]:
            if b != a:
                for rB in list(set(active_res_dic[a][b])):
                    tbwB.append('( resid %i and segid %s )' % (rB, b))
        print '\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB))
        # out.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
# out.close()

            # print e,c
    # print len(interface_res_dic[e])


active_res_dic = dict([(chain, map(int, list(set(interface_res_dic[chain])))) for chain in interface_res_dic])

out = open('active.list','w')
for chain in active_res_dic:
    # print chain, unbound_active_res_dic[chain]
    out.write('sele %s, chain %s and resid %s\n' % (chain, chain, '+'.join(map(str, active_res_dic[chain]))))
out.close()


# generate ambig.tbl
out = open('ambig.tbl','w')
for a in chain_list:
    for rA in list(set(active_res_dic[a])):
        tbwA = 'resid %i and segid %s' % (rA, a)
        tbwB = []
        for b in chain_list:
            if b != a:
                for rB in list(set(active_res_dic[b])):
                    tbwB.append('( resid %i and segid %s )' % (rB, b))
        out.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
out.close()


import subprocess
def run(cmd, outputf):
    with open("./%s" % outputf, "w") as f:
        process = subprocess.Popen(cmd.split(), shell=False, stdout=f)
        process.wait()

for chain in chain_list:
    # python ~/pdb-tools/pdb_selchain.py -J ensemble_1.pdb > J.pdb
    run('python /Users/rvhonorato/pdb-tools/pdb_selchain.py -%s ensemble_1.pdb' % chain, '%s.pdb' % chain)
    run('python /Users/rvhonorato/Nostromo/aa2cg/aa2cg-prot_dna.py %s.pdb' % chain, 'log')
