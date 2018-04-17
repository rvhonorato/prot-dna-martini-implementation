# generate restraints for the 10mer


pdbf = 'ensemble_1.pdb'
contactf = 'ensemble_1_3.0.contacts'
# outf = 'ambig-new-3.0.tbl'

# get chains
chain_list = list(set([l[21] for l in open(pdbf).readlines() if 'ATOM' in l [:4]]))
chain_list.sort()

# crate a dictionary and populate with 
interface_res_dic = dict([(c, {}) for c in chain_list])
unpaired_interface_res_dic = dict([(c, []) for c in chain_list])
for l in open(contactf):
    resA, chainA, atomA, resB, chainB, atomB, dist = l.split()
    #
    resA = int(resA)
    resB = int(resB)
    # first set
    try:
        interface_res_dic[chainA][resA].append(chainB)
    except:
        interface_res_dic[chainA][resA] = []
        interface_res_dic[chainA][resA].append(chainB)
    # second set
    try:
        interface_res_dic[chainB][resB].append(chainA)
    except:
        interface_res_dic[chainB][resB] = []
        interface_res_dic[chainB][resB].append(chainA)
    # unpaired
    unpaired_interface_res_dic[chainA].append(resA)
    unpaired_interface_res_dic[chainB].append(resB)


# 1. Define restraints according to the interface pairing
#  Ex. Chain A has contacts with B, C and F
#    resid resA segidA ( assign ( active res B) ( active res F) )
out = open('ambig-paired.tbl','w')
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

# 2. Define restraints without taking into account interface pairing
#   resis resA segidA ( assign ( active resB )( active resC ) ... ( active resF ) )
out = open('ambig-unpaired.tbl','w')
for chainA in unpaired_interface_res_dic:
    reslistA = list(set(unpaired_interface_res_dic[chainA]))
    for resA in reslistA:
        tbwA = 'resid %i and segid %s' % (resA, chainA)
        #
        tbwB = []
        for chainB in unpaired_interface_res_dic:
            if chainA != chainB:
                reslistB = list(set(unpaired_interface_res_dic[chainB]))
                for resB in reslistB:
                    tbwB.append('( resid %i and segid %s )' % (resB, chainB))
        # print '\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB))
        out.write('\nassign ( %s ) \n(\n %s \n) 2.0 2.0 0.0\n' % (tbwA, '\n or '.join(tbwB)))
out.close









