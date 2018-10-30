# martinize restraints
import sys, re

def identify_bead(atom):
    found_bead = None
    for bead in bead_atom_dic:
        if atom in bead_atom_dic[bead]:
            found_bead = bead
            break
    return found_bead

bead_atom_dic = {
    "BB1": ["CA", "C", "N", "O", "P", "O1P", "O2P", "O5'", "OP1", "OP2"],
    "BB2": ["C5'", "O4'", "C4'"],
    "BB3": ["C3'", "C2'", "C1'"],
    "SC1": ['ND2', 'NE1', 'OG', 'CB', 'OD2', 'CG', 'CE', 'CD', 'CG1', 'NE2', 'CD1', 'CD2', 'OD1', 'OE2', 'ND1', 'OG1', 'CG2', 'SG', 'OE1', 'SD', "N9", "C4", "N1", "C6"],
    "SC2": ['CD2', 'NE', 'CE', 'CZ', 'NZ', 'NH1', 'CE2', 'CE1', 'NH2', 'NE1', 'NE2', 'CD1',"O2", "C2", "N2", "N3"],
    "SC3": ['OH', 'CZ3', 'CZ', 'CE3', 'CE1', 'ND1','C7', 'N6', 'O6', 'N1', 'O4', 'N4', 'C6', 'C5', 'C4'],
    "SC4": ["C8", "N7", "C5", "CZ2","CH2"]
}
# atoms that break the script
blacklist_atoms = ['ZN']

# add wildcard variants
cns_wildcards = ['*','%','#','+']
# "#" matches any string consisting of numerals,
#  this means that C# is C1
Question for the CNS experts: I'm working on a script to convert AA restraints to CG and just came across wildcards; ' \
                               the manual says that #

                               '' \
                               '' \
                               'for th

# fix this! C<int> becomes BB and it should be SC

for bead in bead_atom_dic:
    atom_list = bead_atom_dic[bead]
    new_atom_list = []

    for e in [a + '*' for a in atom_list]:
         new_atom_list.append(e)

    for e in [a + '#' for a in atom_list]:
        new_atom_list.append(e)

    bead_atom_dic[bead] = atom_list + new_atom_list

f = sys.argv[1]

s = ''.join(open(f).readlines()) #.replace('\n','')

for b in blacklist_atoms:
    if b in s:
        print('ERROR: This script cannot handle %s, remove them from %s and try again' % (b, f))
        exit()

# make sure there is room for beads..!
done_list = []
total = len(re.findall(r"name\s*(\w*[^\)])", s))
atom_dic = {}
for i in range(total):
    atoms_match = re.finditer(r"name\s*(\w*[^\)|\s])", s)
    for atom_mNum, atom_m in enumerate(atoms_match):
        if atom_mNum not in done_list:
            atom_start = atom_m.start(1)
            atom_end = atom_m.end(1)
            atom_name = atom_m.group(1)
            new_atom = atom_name + ' ' * (4 - len(str(atom_name)))
            s = s[:atom_start] + new_atom + s[atom_end:] # +1 is the space
            done_list.append(atom_mNum)
            # prepare dictionary for next step
            atom_dic[atom_start] = atom_name, None
            break


# relate atoms with beads
deleted = []
for coord in atom_dic:
    atom = atom_dic[coord][0]
    bead = identify_bead(atom)
    atom_dic[coord] = atom, bead
    if bead == None:

        if atom not in deleted:
            deleted.append(atom)

        # find where it starts
        e =  re.finditer(r"(or\sname$|\(\s*name\s*\))",s[:coord-1])
        start = [j.start() for j in e][0]
        end = coord

        s = s[:start] + '_'*(end-start+len(atom)) + s[end+len(atom):]

    else:
        s = s[:coord] + bead + s[coord+3:]

s = s.replace('_', '')

# print('WARNING the following atoms do not have bead counterparts and were deleted: %s' % ' '.join(deleted))

print(s)