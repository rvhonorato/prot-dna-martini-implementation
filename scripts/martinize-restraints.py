# martinize restraints
import sys, re

bead_atom_dic = {
    "BB1": ["CA", "C", "N", "O", "P", "O1P", "O2P", "O5'", "OP1", "OP2"],
    "BB2": ["C5'", "O4'", "C4'"],
    "BB3": ["C3'", "C2'", "C1'"],
    "SC1": ['ND2', 'NE1', 'OG', 'CB', 'OD2', 'CG', 'CE', 'CD', 'CG1', 'NE2', 'CD1', 'CD2', 'OD1', 'OE2', 'ND1', 'OG1', 'CG2', 'SG', 'OE1', 'SD', "N9", "C4", "N1", "C6"],
    "SC2": ['CD2', 'NE', 'CE', 'CZ', 'NZ', 'NH1', 'CE2', 'CE1', 'NH2', 'NE1', 'NE2', 'CD1',"O2", "C2", "N2", "N3"],
    "SC3": ['OH', 'CZ3', 'CZ', 'CE3', 'CE1', 'ND1','C7', 'N6', 'O6', 'N1', 'O4', 'N4', 'C6', 'C5', 'C4'],
    "SC4": ["C8", "N7", "C5", "CZ2","CH2"]
}

f = sys.argv[1]
out = open('%s' % f.replace('.tbl','-cg.tbl'),'w')

for line in open(f).readlines():

    atoms = set(re.findall(r"name\s(\S*)\s", line))


    if atoms:
        # improve the logic o this?
        ref_dic = {}
        for atom in atoms:
            ref_dic[atom] = None
            for bead in bead_atom_dic:
                if atom in bead_atom_dic[bead]:
                    ref_dic[atom] = bead

        for atom in ref_dic:
            line = line.replace(atom, ref_dic[atom])

    out.write(line)

out.close()
