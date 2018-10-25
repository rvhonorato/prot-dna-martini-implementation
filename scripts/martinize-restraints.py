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
# add wildcard variants
cns_wildcards = ['*','%','#','+']

for bead in bead_atom_dic:
    atom_list = bead_atom_dic[bead]
    new_atom_list = []

    for e in [a + '*' for a in atom_list]:
         new_atom_list.append(e)

    for atom in atom_list:
        try:
            _ = int(atom[-1])
            new_atom_list.append(atom + '#')
        except:
            pass

        try:
            _ = int(atom[-2])
            new_atom_list.append(atom + '#')
        except:
            pass

    bead_atom_dic[bead] = atom_list + new_atom_list

# f = sys.argv[1]
f = '/home/rodrigo/nucleosome/capri/cg-runs/T95-DNA-only-fcc/ambig.tbl'
out = open('%s' % f.replace('.tbl','-cg.tbl'),'w')


for line in open(f):

    # line = 'assign ( resid 262  and segid B )'

    if re.findall(r"\((name.*)\)\)", line):

        matches = re.finditer(r"name\s(.|..|...|....)[\)|\s]", line)
        atoms = [m.group(1) for m in matches]
        # atoms = [a.split(w)[0] for a in atoms for w in  if w in a]

        ref_dic = {}
        for atom in atoms:
            ref_dic[atom] = ''
            for bead in bead_atom_dic:
                if atom in bead_atom_dic[bead]:
                    ref_dic[atom] = bead

        for atom in ref_dic:

            regex = r"(name %s)[\s|\)]" % atom
            
            for c in cns_wildcards:
                if c in atom:
                    regex = r"(name %s)[\s|\)]" % atom.replace(c, '\%s' % c)
                    break

            e = re.finditer(regex, line)
            start, end = [(j.start(), j.end()) for j in e][0]

            bead = ref_dic[atom]


            if bead:
                line = line[:start] + 'name ' + bead + ' ' + line[end:]
            else:
                line = line[:start] + '' + line[end:]

        # look for syntax errors
        line = line.replace('or or','or')
        line = line.replace('or )', ')')
        line = line.replace('or)', ')')

    else:
        pass

    out.write(line)

out.close()
