def identify_pairing(rA, rB, Basedist_cutoff):
# rename_dic = {}
renumber_dic = {}

# check if the pairing is correct

rA_name = rA.resname
rB_name = rB.resname
#
try:
    atom_pair_list = pairing[rA_name, rB_name]
except KeyError:
    # pairing not possible
    return

# check if distances are ok
distance_l = []
for atom_list in atom_pair_list:
    a = rA[atom_list[0]]
    b = rB[atom_list[1]]
    distance_l.append(a-b)

if [ e for e in distance_l if e < Basedist_cutoff ]: # if any bond is withing range
    #
    # special atoms, mark them!
    #
    # atomlistA = rA.
    # atomlistB = 
    # print atom_pair_list, rA.resname, rB.resname, rA, rB
    for atom_pair in atom_pair_list:
        atomA, atomB = atom_pair
        #
        rA[atomA].bfactor = 1
        rB[atomB].bfactor = 1
    # # atomsA = [rA[a[0]] for a in atom_pair_list]
    # # atomsB = [rB[a[1]] for a in atom_pair_list]
    # #
    # # return atom_pair_list, rA.resname, rB.resname
    # exit()
    # # if not 'h' in rA.resname:
    # #     rename_dic[rA] = 'h' + rA.resname.split()[0]
    # # if not 'h' in rB.resname:
    # #     rename_dic[rB] = 'h' + rB.resname.split()[0]
    # # if not 'h' in rA.resname:
    # renumber_dic[rA] = 1
    # # if not 'h' in rB.resname:
    # renumber_dic[rB] = 1
# else:
    # print rA, rB, distance_l, [ e for e in distance_l if e < 3.5 ]

return renumber_dic

# def rename_res(resdic):
#     for r in resdic:
#         r.resname = resdic[r]

# def change_bfactor(resdic):

def determine_hbonds(structure):

nuc = ['DA', 'DC', 'DG', 'DT']
# hb_nuc = ['hDA', 'hDC', 'hDG', 'hDT']
aa = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS", "LEU", "MET", "ASN", "PRO", "GLN", "ARG", "SER", "THR", "VAL", "TRP", "TYR"] 

distance_cutoff = 3.5

renumber_list = []

for model in structure:
    dna_chain_l = []
    for chain in model:
        prot_comp = len([r for r in chain.get_residues() if r.resname.split()[0] in aa])
        dna_comp =  len([r for r in chain.get_residues() if r.resname.split()[0] in nuc])
        if prot_comp:
            # print chain, 'is protein'
            pass
        if dna_comp:
            # print chain, 'is nucleic'
            dna_chain_l.append(chain)
        if dna_comp and prot_comp:
            print chain, 'is mixed nucleic/protein, not supported'
            exit()
    if len(dna_chain_l) == 1:
        print ' WARNING: Only one DNA chain detected, is this correct?'
        chainA = dna_chain_l[0]
        reslistA = [r for r in chainA.get_residues()]
        for rA, rB in itertools.combinations(reslistA, 2):
            # print rA.id[1], rB.id[1]
            print rA, rB


#             identify_pairing(rA, rB, distance_cutoff)
#             # if paired_dna_dic:
#             #     # print rA, rB
#             #     # print paired_dna_dic.keys()
#             #     rename_res(paired_dna_dic)
#             #     # #
#             #     # for r in paired_dna_dic:
#             #     #     renumber_list.append(r.id[1])


#     if len(dna_chain_l) > 1:   ## list sizes could be different, this might be improvable
#         for chainA, chainB in itertools.combinations(dna_chain_l, 2):
#             reslistA = [r for r in chainA.get_residues()]
#             reslistB = [r for r in chainB.get_residues()]
#             for rA in reslistA:
#                 atomlistA = rA.child_dict.values()
#                 for rB in reslistB:
#                     identify_pairing(rA, rB, distance_cutoff)
#                     # if paired_dna_dic:
#                         # rename_res(paired_dna_dic)            
# return structure, renumber_list
