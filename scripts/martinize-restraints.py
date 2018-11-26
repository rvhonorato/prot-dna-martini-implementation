# martinize restraints
import sys, re, argparse

def identify_bead(atom):
    # found_bead = None
    found_bead = []
    for bead in bead_atom_dic:
        if atom in bead_atom_dic[bead]:
            found_bead.append(bead)
            # break
    return found_bead

bead_atom_dic = {
    "BB": ["CA", "C", "N", "O"],
    "BB1": ["P", "O1P", "O2P", "O5'", "OP1", "OP2"],
    "BB2": ["C5'", "O4'", "C4'"],
    "BB3": ["C3'", "C2'", "C1'"],
    "SC1": ['ND2', 'NE1', 'OG', 'CB', 'OD2', 'CG', 'CE', 'CD', 'CG1', 'NE2', 'CD1', 'CD2', 'OD1', 'OE2', 'ND1', 'OG1', 'CG2', 'SG', 'OE1', 'SD', "N9", "C4", "N1", "C6"],
    "SC2": ['CD2', 'NE', 'CE', 'CZ', 'NZ', 'NH1', 'CE2', 'CE1', 'NH2', 'NE1', 'NE2', 'CD1',"O2", "C2", "N2", "N3"],
    "SC3": ['OH', 'CZ3', 'CZ', 'CE3', 'CE1', 'ND1','C7', 'N6', 'O6', 'N1', 'O4', 'N4', 'C6', 'C5', 'C4'],
    "SC4": ["C8", "N7", "C5", "CZ2","CH2"]
}
# atoms that break the script
blacklist_atoms = ['ZN']

#
# for b in blacklist_atoms:
#     if b in s:
#         print('ERROR: This script cannot handle %s, remove them from %s and try again' % (b, f))
#         exit()

# add wildcard variants
cns_wildcards = ['*','%','#','+']
# "#" matches any string consisting of numerals,
#  this means that C# is C1


import argparse


parser = argparse.ArgumentParser()

parser.add_argument("rest_file", type=str,
                    help="AIR file")

parser.add_argument("--ambig", help="Ambiguous",
                    action="store_true")

parser.add_argument("--unambig", help="Unambiguous",
                    action="store_true")

args = parser.parse_args()

if not args.ambig and not args.unambig:
    print parser.print_help()

# fix this! C<int> becomes BB and it should be SC
for bead in bead_atom_dic:
    atom_list = bead_atom_dic[bead]
    new_atom_list = []
    for e in atom_list:
        # print(e)
        for i, s in enumerate(e):
            check = None
            try:
                check = int(list(e)[i + 1])
            except:
                pass
            #
            if check:
                new_atom = ''.join(list(e)[:i + 1]) + '#'
                new_atom_list.append(new_atom)

            if i + 1 < len(e):
                new_atom = ''.join(list(e)[:i + 1]) + '*'
                new_atom_list.append(new_atom)

    bead_atom_dic[bead] = list(set(atom_list + new_atom_list))

# f = sys.argv[1]
f = args.rest_file
# f = '/home/rodrigo/tmp/unambig.tbl'

s = ''.join(open(f).readlines()) #.replace('\n','')
s = s.replace('\n','')

import regex
str_match = regex.match(r"(assign\s\(.*?\d*\.\d*\s*\d*\.\d*\s*\d*\.\d*)++", s)

if args.unambig:

    for assign_str in str_match.captures(1):

        num_regex = r"(\d*\.\d*\s\d*\.\d*\s*\d*\.\d*)"
        nums_l = map(float, re.findall(num_regex, assign_str)[0].split())

    # if unambig:
    # if args.unambig:
        regex = r"\([^)]*\)"
        rest_dic = {}
        for i, e in enumerate(re.findall(regex, assign_str)):
            resid = int(re.findall(r"resid\s*(\d*)", e)[0])
            segid = re.findall(r"segid\s*(\w*)", e)[0]
            atom_list = re.findall(r"name\s*(\w*)", e) # keep it as a list
            try:
                syntax = re.findall(r"and (not)", e)[0]
            except IndexError:
                syntax = None
            rest_dic[i] = resid, segid, syntax, atom_list, []

        # print rest_dic

        # martinize!
        for idx in rest_dic:
            atom_list = rest_dic[idx][3]
            bead_list = []
            for atom in atom_list:
                for bead in identify_bead(atom):
                    bead_list.append(bead)
            _ = [rest_dic[idx][4].append(b) for b in set(bead_list)]

        # write
        rest_str = 'assign '
        for idx in rest_dic:
            rest_str += '( '
            resid = rest_dic[idx][0]
            segid = rest_dic[idx][1]
            bead_l = rest_dic[idx][4]
            rest_str += ' resid %s and segid %s ' % (resid, segid)
            if bead_l:
                if syntax:
                    rest_str += '%s '
                else:
                    rest_str += 'and '
                rest_str += '( %s )' % ('name ' + ' or name '.join(bead_l))
            rest_str += ') '
            # tbw.append(rest_str)
        rest_str += ' '.join(['%.3f'%e for e in nums_l])
        print rest_str

if args.ambig:
    for assign_str in str_match.captures(1):
        num_regex = r"(\d*\.\d*\s\d*\.\d*\s*\d*\.\d*)"
        nums_l = map(float, re.findall(num_regex, assign_str)[0].split())

        regex = r"resid\s*(\d*)\s*and\s*segid\s*(\w*)\s*(and|and not)?(?(3)\s(\([^)]*\))|)\)"
        matches = re.finditer(regex, assign_str)

        # for n, match in enumerate(matches):
        rest_dic = {}
        for num, m in enumerate(matches):
            if num == 0: # match0 is the active residue
                act_resid = int(m.group(1))
                act_segid = m.group(2)
                try:
                    act_syntax = m.group(3)
                    act_atom_list = m.group(4)
                    act_atom_list = re.findall(r"name\s*(\w*)", ''.join(act_atom_list))
                except IndexError:
                    act_syntax = None
                    act_atom_list = None
                #
                rest_dic[num] = act_resid, act_segid, act_syntax, act_atom_list, [], {}
            else:
                resid = int(m.group(1))
                segid = m.group(2)
                try:
                    syntax = m.group(3)
                    atom_list = m.group(4)
                    atom_list = re.findall(r"name\s*(\w*)", ''.join(atom_list))
                except:
                    syntax = None
                    atom_list = None
                #
                rest_dic[0][-1][num] = resid, segid, syntax, atom_list, []

        # martinize!

        for idx in rest_dic:
            atom_list = rest_dic[idx][3]
            bead_list = []
            for atom in atom_list:
                for bead in identify_bead(atom):
                    bead_list.append(bead)
            _ = [rest_dic[idx][4].append(b) for b in set(bead_list)]
            rdic = rest_dic[idx][-1]
            for rkey in rdic:
                ratom_list = rdic[rkey][3]
                rbead_list = []
                if ratom_list:
                    for ratom in ratom_list:
                        for rbead in identify_bead(ratom):
                            rbead_list.append(rbead)
                    _ = [rdic[rkey][4].append(rb) for rb in set(rbead_list)]

        # re-write...!
        # print 'assign (resid %i and segid %s) (' % (rest_dic[0][0], rest_dic[0][1])
        ass_resid = rest_dic[0][0]
        ass_segid = rest_dic[0][1]
        ass_syntax = rest_dic[0][2]
        ass_bead_list = rest_dic[0][4]

        ass_str = 'assign (resid %i and segid %s ' % (ass_resid, ass_segid)
        if ass_syntax:
            ass_str += '%s ( %s ) ) (' % (ass_syntax, ('name ' + ' or name '.join(ass_bead_list)))
            # print(ass_str)
            # exit()
        else:
            ass_str += ') ( '

        tbw = []
        for idx in rest_dic[0][-1]:
            rest_str = '( '
            resid = rest_dic[0][-1][idx][0]
            segid = rest_dic[0][-1][idx][1]
            syntax = rest_dic[0][-1][idx][2]
            atom_l = rest_dic[0][-1][idx][3]
            bead_l = rest_dic[0][-1][idx][4]

            rest_str += 'resid %s and segid %s ' % (resid, segid)
            if syntax:
                bead_l.sort()
                rest_str += ' %s ( %s )' % (syntax , ('name ' + ' or name '.join(bead_l)))
                # print(rest_str)
            rest_str += ' )'
            tbw.append(rest_str)

        print ass_str
        print '\n or '.join(tbw)
        print ')' + ' '.join(['%.3f'%e for e in nums_l])
        print '\n'

