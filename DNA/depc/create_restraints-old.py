# get protein interface from complex, define all DNA as active

# generate restraints for the 10mer
import sys, glob

# everything must have the same chain ids
pdbf = sys.argv[1]
contactf = sys.argv[2]

dna_chain = 'B'

# load numbering reference
numbering_dic = {}
for f in glob.glob('*numbering.ref'):
    # open(f).readlines()
    chain = f.split('-')[0]
    numbering_dic[chain] = dict([map(int, a.split(',')) for a in open(f)])

# get chains
chain_list = list(set([l[21] for l in open(pdbf).readlines() if 'ATOM' in l [:4]]))
chain_list.sort()

# crate a dictionary and populate with 
interface_res_dic = dict([(c, {}) for c in chain_list])
unpaired_interface_res_dic = dict([(c, []) for c in chain_list])
for l in open(contactf):
    bound_resA, chainA, _, bound_resB, chainB, _, dist = l.split()
    #
    bound_resA = int(bound_resA)
    bound_resB = int(bound_resB)
    # look for unbound equivalents...
    try:
        unbound_resA = numbering_dic[chainA][bound_resA]
        unbound_resB = numbering_dic[chainB][bound_resB]
    except:
        # no correspondence found
        continue
    #

    # first set
    try:
        interface_res_dic[chainA][unbound_resA].append(chainB)
    except:
        interface_res_dic[chainA][unbound_resA] = []
        interface_res_dic[chainA][unbound_resA].append(chainB)
    # second set
    try:
        interface_res_dic[chainB][unbound_resB].append(chainA)
    except:
        interface_res_dic[chainB][unbound_resB] = []
        interface_res_dic[chainB][unbound_resB].append(chainA)
    # unpaired
    unpaired_interface_res_dic[chainA].append(unbound_resA)
    unpaired_interface_res_dic[chainB].append(unbound_resB)


# hack to define all DNA as active
dna_reslist = list(set(map(int, [l[22:26] for l in open(pdbf).readlines() if l[:4] == 'ATOM' and l[21] == dna_chain])))
interface_res_dic[dna_chain] = dict([(r, ['A']) for r in dna_reslist])

[(a, ','.join(map(str, interface_res_dic[a]))) for a in interface_res_dic]

# 1. Define restraints according to the interface pairing
#  Ex. Chain A has contacts with B, C and F
#    resid resA segidA ( assign ( active res B) ( active res F) )
out = open('dna-active-ambig.tbl','w')
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

# # 2. Define restraints without taking into account interface pairing
# #   resis resA segidA ( assign ( active resB )( active resC ) ... ( active resF ) )
# out = open('ambig-unpaired.tbl','w')
# for chainA in unpaired_interface_res_dic:
#     reslistA = list(set(unpaired_interface_res_dic[chainA]))
#     for resA in reslistA:
#         tbwA = 'resid %i and segid %s' % (resA, chainA)
#         #
#         tbwB = []
#         for chainB in unpaired_interface_res_dic:
#             if chainA != chainB:
#                 reslistB = list(set(unpaired_interface_res_dic[chainB]))
#                 for resB in reslistB:
#                     tbwB.append('( resid %i and segid %s )' % (resB, chainB))
#         # print '\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB))
#         out.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
# out.close









