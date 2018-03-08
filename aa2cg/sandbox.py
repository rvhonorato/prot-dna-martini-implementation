"""
Reduces complexity of protein residue to the MARTINI coarse grained model:
CA, O, Bead(s) in specific atom location.

Reference:
Monticelli et al. The MARTINI coarse-grained force field: extension to proteins. 
J. Chem. Theory Comput. (2008) vol. 4 (5) pp. 819-834

Martinize Script from Tserk Wassenaar
"""
polar   = ["GLN","ASN","SER","THR"]
charged = ["ARG", "LYS","ASP","GLU"]
bb = "CA C N O "
prot_atoms = {      "ALA":  [bb + "CB"],
                    "CYS":  [bb, "CB SG"],
                    "ASP":  [bb, "CB CG OD1 OD2"],
                    "GLU":  [bb, "CB CG CD OE1 OE2"],
                    "PHE":  [bb, "CB CG CD1","CD2 CE2","CE1 CZ"],
                    "GLY":  [bb],
                    "HIS":  [bb, "CB CG","CD2 NE2","ND1 CE1"],
                    "ILE":  [bb, "CB CG1 CG2 CD1"],
                    "LYS":  [bb, "CB CG CD","CE NZ"],
                    "LEU":  [bb, "CB CG CD1 CD2"],
                    "MET":  [bb, "CB CG SD CE"],
                    "ASN":  [bb, "CB CG ND1 ND2 OD1 OD2"], #ND1?
                    "PRO":  [bb, "CB CG CD"],
                    "GLN":  [bb, "CB CG CD OE1 OE2 NE1 NE2"],
                    "ARG":  [bb, "CB CG CD","NE CZ NH1 NH2"],    
                    "SER":  [bb, "CB OG"],
                    "THR":  [bb, "CB OG1 CG2"],
                    "VAL":  [bb, "CB CG1 CG2"],
                    "TRP":  [bb, "CB CG CD2","CD1 NE1 CE2","CE3 CZ3","CZ2 CH2"],
                    "TYR":  [bb, "CB CG CD1","CD2 CE2","CE1 CZ OH"]}

bead_names = [" BB", " SC1", " SC2", " SC3", " SC4"] # Space bc of IO issues.

# insert beads into the data structure
cg_mapping = {}
for res in prot_atoms:
    cg_mapping[res] = {}
    for i, atom_l in enumerate(prot_atoms[res]):
        bead = bead_names[i]
        cg_mapping[res][atom_l] = bead


dna_bead_dic = {' DC':
{
    "P OP1 OP2 O5' O3'": "Q0",
    "C5' O4' C4'":       "SN0",
    "C3' C2' C1'":       "SC2",
    #
    "N1 C6":             "TN0",
    "N3 C2 O2":          "TY2", 
    "C5 C4 N4":          "TY3"
},
                ' DA':
{
    "P OP1 OP2 O5' O3'": "Q0",
    "C5' O4' C4'":       "SN0",
    "C3' C2' C1'":       "SC2",
    #
    "N9 C4":             "TN0",
    "C2 N3":             "TA2",
    "C6 N6 N1":          "TA3",
    "C8 N7 C5":          "TNa"
},
                ' DG':
{
    "P OP1 OP2 O5' O3'": "Q0",
    "C5' O4' C4'":       "SN0",
    "C3' C2' C1'":       "SC2",
    #
    "N9 C4":             "TN0",
    "C2 N2 N3":          "TG2",
    "C6 O6 N1":          "TG3",
    "C8 N7 C5":          "TNa"
},
                ' DT':
{
    "P OP1 OP2 O5' O3'": "Q0",
    "C5' O4' C4'":       "SN0",
    "C3' C2' C1'":       "SC2",
    #
    "N1 C6":             "TN0",
    "N3 C2 O2":          "TT2",
    "C5 C4 O4 C7":       "TT3"
}
}

cg_mapping[' DA'] = dna_bead_dic[' DA']
cg_mapping[' DC'] = dna_bead_dic[' DC']
cg_mapping[' DT'] = dna_bead_dic[' DT']
cg_mapping[' DG'] = dna_bead_dic[' DG']

resn = aares.resname
segid = aares.segid.strip() 
resi = aares.id[1]

beads = []
cg_to_aa_restraints = []
# cg_mapping = n_d
# print cg_mapping[resn]
for atom_segment in sorted(cg_mapping[resn].items(), key=operator.itemgetter(0)):
    bead = cg_mapping[resn][atom_segment[0]]
    atoms = [aares[a] for a in atom_segment[0].split() if a in aares.child_dict]
    if not atoms:
        print 'Residue %(resn)s%(resi)s of chain %(chain)s cannot be processed: missing atoms (%(centroid)s)\n' %locals()
        continue
    bcom = center_of_mass(atoms)
    # [aares[atom] for atom in centroid.split() if atom in aares.child_dict]
    beads.append((bead, bcom))
    cg_to_aa_restraints.append("assign (segid %sCG and resid %i and name %s) (segid %s and resid %i and (name %s)) 0 0 0" %(segid, resi, bead, segid, resi, ' or name '.join(atom_segment[0].split(' '))))
    #
    # print [aares[a] for a in atoms[0].split()]
    # print bcom
    # exit()

if len(beads) > 1 and resn in polar:
    beads = add_dummy(beads, dist=0.14, n=2)
if len(beads) > 1 and resn in charged:  
    beads = add_dummy(beads, dist=0.11, n=1)