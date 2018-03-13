#!/usr/bin/env python2.6
"""
Uses Biopython to parse the structure and DSSP output.
Uses pieces of the martinize-1.1.py script to convert the SS types

Outputs a coarse grained pdb file (*_ss.pdb) with assigned bfactors.
Outputs a tbl file to map the beads to the atoms they represent.

Updates
 - Updated python version to 2.6 to support isdisjoint() set method in DSSP.py (JR Apr 2012)
 - Residues that DSSP can't handle (incomplete backbone f ex) treated as coil  (JR Apr 2012)
 - Update to_one_letter_code library to protein_letters_3to1 (Jorge Roel 2017)
 - Inclusion of fake beads for corresponding amino-acids <SCd> (Jorge Roel 2017)
 - Implemented feature to check if nucleic acid is a candidate for hbond (Rodrigo Honorato 2018)
 - Changed the mapping routine to include DNA and hbond DNA bead types (Rodrifo Honorato 2018)
"""
import os
import sys
import random
import math
import operator #
import itertools #
import collections
import warnings
warnings.filterwarnings("ignore")

try:
  from Bio.PDB import PDBParser
  from Bio.PDB import PDBIO
  from Bio.PDB.DSSP import DSSP
  from Bio.PDB import Entity
#  from Bio.PDB import to_one_letter_code 
  from Bio.PDB import protein_letters_3to1
  from Bio.PDB.StructureBuilder import StructureBuilder
except ImportError, emsg:
    sys.stderr.write('Error: %s\n' %emsg)
    sys.stderr.write("Error loading Biopython. Make sure it's on your PYTHONPATH\n")
    sys.exit(1)

##########################
## CG STRUCTURE BUILDER ##
##########################

def center_of_mass(entity, geometric=False):
    """
    Returns gravitic [default] or geometric center of mass of an Entity.
    Geometric assumes all masses are equal (geometric=True)
    """

    # Structure, Model, Chain, Residue
    if isinstance(entity, Entity.Entity):
        atom_list = entity.get_atoms()
    # List of Atoms
    elif hasattr(entity, '__iter__') and [x for x in entity if x.level == 'A']:
        atom_list = entity
    else: # Some other weirdo object
        raise ValueError("Center of Mass can only be calculated from the following objects:\n"
                            "Structure, Model, Chain, Residue, list of Atoms.")
    
    masses = []
    positions = [ [], [], [] ] # [ [X1, X2, ..] , [Y1, Y2, ...] , [Z1, Z2, ...] ]
    
    for atom in atom_list:
        masses.append(atom.mass)
        
        for i, coord in enumerate(atom.coord.tolist()):
            positions[i].append(coord)

    # If there is a single atom with undefined mass complain loudly.
    if 'ukn' in set(masses) and not geometric:
        raise ValueError("Some Atoms don't have an element assigned.\n"
                         "Try adding them manually or calculate the geometrical center of mass instead.")
    
    if geometric:
        return [sum(coord_list)/len(masses) for coord_list in positions]
    else:       
        w_pos = [ [], [], [] ]
        for atom_index, atom_mass in enumerate(masses):
            w_pos[0].append(positions[0][atom_index]*atom_mass)
            w_pos[1].append(positions[1][atom_index]*atom_mass)
            w_pos[2].append(positions[2][atom_index]*atom_mass)

        return [sum(coord_list)/sum(masses) for coord_list in w_pos]

def norm(a):
    return math.sqrt(norm2(a))

def norm2(a):
    return sum([i*i for i in a])

def add_dummy(beads, dist=0.11, n=2):
    # Generate a random vector in a sphere of -1 to +1, to add to the bead position
    v    = [random.random()*2.-1, random.random()*2.-1, random.random()*2.-1]
    # Calculated the length of the vector and divide by the final distance of the dummy bead
    norm_v = norm(v)/dist
    # Resize the vector
    vn   = [i/norm_v for i in v]
    # m sets the direction of the added vector, currently only works when adding one or two beads.
    m = 1
    for j in range(n):
        newName = 'SCD' + str(j+1)
        newBead = (newName, [i+(m*j) for i, j in zip(beads[-1][1], vn)])
        beads.append(newBead)
        m *= -2
    return beads


## Coarse Graining

def mapcg(aares):    
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

    bead_names = ["BB", "SC1", "SC2", "SC3", "SC4"] # Space bc of IO issues.

    # insert beads into the data structure
    cg_mapping = {}
    for res in prot_atoms:
        cg_mapping[res] = {}
        for i, atom_l in enumerate(prot_atoms[res]):
            bead = bead_names[i]
            cg_mapping[res][atom_l] = bead


    # Define nucleotide mapping,
    ## This is a custom naming convetion
    ##  but the atom mapping is defined in
    ##   10.1021/acs.jctc.5b00286 -  S1
    ######################################
    DC_beads = collections.OrderedDict()
    DC_beads["P OP1 OP2 O5' O3'"] =  "nB0"
    DC_beads["C5' O4' C4'"] =        "nB1"
    DC_beads["C3' C2' C1'"] =        "nB2"
    DC_beads["N1 C6"] =              "S4"
    DC_beads["N3 C2 O2"] =           "S8" 
    DC_beads["C5 C4 N4"] =           "S9"

    hDC_beads = collections.OrderedDict()
    hDC_beads["P OP1 OP2 O5' O3'"] = "nB0"
    hDC_beads["C5' O4' C4'"] =       "nB1"
    hDC_beads["C3' C2' C1'"] =       "nB2"
    hDC_beads["N1 C6"] =             "S4"
    hDC_beads["N3 C2 O2"] =          "H6"
    hDC_beads["C5 C4 N4"] =          "H7"

    DA_beads = collections.OrderedDict()
    DA_beads["P OP1 OP2 O5' O3'"] =  "nB0"
    DA_beads["C5' O4' C4'"] =        "nB1"
    DA_beads["C3' C2' C1'"] =        "nB2"
    DA_beads["N9 C4"] =              "S4"
    DA_beads["C2 N3"] =              "S0"
    DA_beads["C6 N6 N1"] =           "S1"
    DA_beads["C8 N7 C5"] =           "S5"

    hDA_beads = collections.OrderedDict()
    hDA_beads["P OP1 OP2 O5' O3'"] = "nB0"
    hDA_beads["P OP1 OP2 O5' O3'"] = "nB0"
    hDA_beads["C5' O4' C4'"] =       "nB1"
    hDA_beads["N9 C4"] =             "S4"
    hDA_beads["C2 N3"] =             "H0"
    hDA_beads["C6 N6 N1"] =          "H1"

    DG_beads = collections.OrderedDict()
    DG_beads["P OP1 OP2 O5' O3'"] =  "nB0"
    DG_beads["C5' O4' C4'"] =        "nB1"
    DG_beads["C3' C2' C1'"] =        "nB2"
    DG_beads["N9 C4"] =              "S4"
    DG_beads["C2 N2 N3"] =           "S2"
    DG_beads["C6 O6 N1"] =           "S3"
    DG_beads["C8 N7 C5"] =           "S5"

    hDG_beads = collections.OrderedDict()
    hDG_beads["P OP1 OP2 O5' O3'"] = "nB0"
    hDG_beads["C5' O4' C4'"] =       "nB1"
    hDG_beads["C3' C2' C1'"] =       "nB2"
    hDG_beads["N9 C4"] =             "S4"
    hDG_beads["C2 N2 N3"] =          "H2"
    hDG_beads["C6 O6 N1"] =          "H3"
    hDG_beads["C8 N7 C5"] =          "S5"

    DT_beads = collections.OrderedDict()
    DT_beads["P OP1 OP2 O5' O3'"] =  "nB1"
    DT_beads["C5' O4' C4'"] =        "nB2"
    DT_beads["C3' C2' C1'"] =        "nB3"
    DT_beads["N1 C6"] =              "S4"
    DT_beads["N3 C2 O2"] =           "S6"
    DT_beads["C5 C4 O4 C7"] =        "S7"

    hDT_beads = collections.OrderedDict()
    hDT_beads["P OP1 OP2 O5' O3'"] = "nB1"
    hDT_beads["C5' O4' C4'"] =       "nB2"
    hDT_beads["C3' C2' C1'"] =       "nB3"
    hDT_beads["N1 C6"] =             "S4"
    hDT_beads["N3 C2 O2"] =          "H4"
    hDT_beads["C5 C4 O4 C7"] =       "H5"


    cg_mapping['DA'] = DA_beads
    cg_mapping['DC'] = DC_beads
    cg_mapping['DT'] = DT_beads
    cg_mapping['DG'] = DG_beads
    cg_mapping['hDA'] = hDA_beads
    cg_mapping['hDC'] = hDC_beads
    cg_mapping['hDT'] = hDT_beads
    cg_mapping['hDG'] = hDG_beads
 
    resn = aares.resname
    segid = aares.segid.strip() 
    resi = aares.id[1]

    beads = []
    cg_to_aa_restraints = []

    for atom_segment in cg_mapping[resn]:
        bead = cg_mapping[resn][atom_segment]
        atoms = [aares[a] for a in atom_segment.split() if a in aares.child_dict]
        if not atoms:
            resi = aares.id[1]
            chain = aares.parent.id
            print 'Residue %(resn)s%(resi)s of chain %(chain)s cannot be processed: missing atoms (%(atom_segment)s)\n' %locals()
            continue
        bcom = center_of_mass(atoms)
        beads.append((bead, bcom))
        cg_to_aa_restraints.append("assign (segid %sCG and resid %i and name %s) (segid %s and resid %i and (name %s)) 0 0 0" %(segid, resi, bead, segid, resi, ' or name '.join(atom_segment[0].split(' '))))

    if len(beads) > 1 and resn in polar:
        beads = add_dummy(beads, dist=0.14, n=2)
    if len(beads) > 1 and resn in charged:  
        beads = add_dummy(beads, dist=0.11, n=1)

    return (cg_to_aa_restraints, beads)


def determine_hbonds(structure):
    nuc = ['DA', 'DC', 'DG', 'DT']
    hb_nuc = ['hDA', 'hDC', 'hDG', 'hDT']
    aa = ["ALA", "CYS", "ASP", "GLU", "PHE", "GLY", "HIS", "ILE", "LYS", "LEU", "MET", "ASN", "PRO", "GLN", "ARG", "SER", "THR", "VAL", "TRP", "TYR"]
    pairing = {'A':'T', 'C':'G', 'T':'A', 'G':'C'}
    #
    # for model in structure:
    model = structure[0]
    #
    dna_chain_l = []
    for chain in model:
        # print chain
        prot_comp = len([r for r in chain.get_residues() if r.resname.split()[0] in aa])
        dna_comp =  len([r for r in chain.get_residues() if r.resname.split()[0] in nuc])
        hbond_dna_comp = len([r for r in chain.get_residues() if r.resname.split()[0] in hb_nuc])
        #
        if prot_comp:
            # print chain, 'is protein'
            pass
        if dna_comp:
            # print chain, 'is nucleic'
            dna_chain_l.append(chain)
        if hbond_dna_comp:
            # print chain, 'is hbond nucleic'
            pass
        if dna_comp and prot_comp:
            print chain, 'is mixed nucleic/protein, investigate'
            exit()
    #
    # check distances!
    ## list sizes could be different, this might be improvable
    distance_cutoff = 3.
    for chainA, chainB in itertools.combinations(dna_chain_l, 2):
        #
        reslistA = [r for r in chainA.get_residues()]
        reslistB = [r for r in chainB.get_residues()]
        #
        for rA in reslistA:
            #
            atomlistA = rA.child_dict.values()
            #
            for rB in reslistB:
                #
                atomlistB = rB.child_dict.values()
                #
                baseA = rA.resname.split()[0][-1]
                baseB = rB.resname.split()[0][-1]
                #
                # do all calculations so we can check if there's an incorrect pairing
                distance_list = [a-b for a in atomlistA for b in atomlistB]
                if min(distance_list) <= distance_cutoff:
                    #
                    if not 'h' in rA.resname:
                        rA.resname = 'h' + rA.resname.split()[0]
                    if not 'h' in rB.resname:
                        rB.resname = 'h' + rB.resname.split()[0]
                    #
                    if pairing[baseA] != baseB:
                        print 'warning, incorrect pairing!'
                        exit()
    return structure 

## SECONDARY STRUCTURE DEFINITION  ## 
##  CODE TAKEN FROM MARTINIZE 1.1  ##

# Function to reformat pattern strings                                        
def pat(x,c="."):                                                             
    return x.replace(c,"\x00").split()

# Make a dictionary from two lists                                            
def hash(x,y):                                                                
    return dict(zip(x,y))

# Split a string                                                              
def spl(x):                                                                   
    return x.split()

#############################
## 5 # SECONDARY STRUCTURE ##  -> @SS <-
#############################


#----+--------------------------------------+
## A | SECONDARY STRUCTURE TYPE DEFINITIONS |
#----+--------------------------------------+

# This table lists all coarse grained secondary structure types
# The following are matched lists. Make sure they stay matched.
# The lists do not need to be of the same length. The longer list
# will be truncated when combined with a shorter list, e.g. with
# dihedral definitions, which are not present for coil and termini
#
ss_names = {
 "F": "Collagenous Fiber",                                                                  #@#
 "E": "Extended structure (beta sheet)",                                                    #@#
 "H": "Helix structure",                                                                    #@#
 "1": "Helix start (H-bond donor)",                                                         #@#
 "2": "Helix end (H-bond acceptor)",                                                        #@#
 "3": "Ambivalent helix type (short helices)",                                              #@#
 "T": "Turn",                                                                               #@#
 "S": "Bend",                                                                               #@#
 "C": "Coil",                                                                               #@#
}

bbss = ss_names.keys()
bbss     =    spl("  F     E     H     1     2     3     T     S     C")  # SS one letter 


# The following dictionary contains secondary structure types as assigned by
# different programs. The corresponding Martini secondary structure types are               
# listed in cgss                                                                            
#                                                                                           
# NOTE:                                                                                     
#  Each list of letters in the dictionary ss should exactly match the list                  
#  in cgss.                                                                                 
#                                                                                           
ssdefs = {
    "dssp":  list(".HGIBETSC~"),             # DSSP one letter secondary structure code     #@#
    "pymol": list(".H...S...L"),             # Pymol one letter secondary structure code    #@# 
    "gmx":   list(".H...ETS.C"),             # Gromacs secondary structure dump code        #@#    
    "self":  list("FHHHEETSCC")              # Internal CG secondary structure codes        #@#
}
cgss     =   list("FHHHEETSCC")              # Corresponding CG secondary structure types   #@#

#----+-------------------------------------------+
## B | SECONDARY STRUCTURE PATTERN SUBSTITUTIONS |
#----+-------------------------------------------+


# For all structure types specific dihedrals may be used if four or
# more consecutive residues are assigned that type.                

# Helix start and end regions are special and require assignment of
# specific types. The following pattern substitutions are applied 
# (in the given order). A dot matches any other type.             
# Patterns can be added to the dictionaries. This only makes sense
# if for each key in patterns there is a matching key in pattypes.
patterns = {
    "H": pat(".H. .HH. .HHH. .HHHH. .HHHHH. .HHHHHH. .HHHHHHH. .HHHH HHHH.")                #@#
}
pattypes = {
    "H": pat(".3. .33. .333. .3333. .13332. .113322. .1113222. .1111 2222.")                #@#
}

# List of programs for which secondary structure definitions can be processed
programs = ssdefs.keys()                                                                    


# Dictionaries mapping ss types to the CG ss types                                          
ssd = dict([ (i, hash(ssdefs[i],cgss)) for i in programs ])                             


# From the secondary structure dictionaries we create translation tables
# with which all secondary structure types can be processed. Anything
# not listed above will be mapped to C (coil).
# Note, a translation table is a list of 256 characters to map standard  
# ascii characters to.
def tt(program):                                                                            
    return  "".join([ssd[program].get(chr(i),"C") for i in range(256)])                     


# The translation table depends on the program used to obtain the 
# secondary structure definitions
sstt = dict([(i,tt(i)) for i in programs])                                                  


# The following translation tables are used to identify stretches of 
# a certain type of secondary structure. These translation tables have
# every character, except for the indicated secondary structure, set to
# \x00. This allows summing the sequences after processing to obtain
# a single sequence summarizing all the features.
null = "\x00"                                                                               
sstd = dict([ (i,ord(i)*null+i+(255-ord(i))*null) for i in cgss ])                          


# Pattern substitutions
def typesub(seq,patterns,types):                                                            
    for i,j in zip(patterns,types):                                                         
        seq = seq.replace(i,j)                                                              
    return seq

# The following function translates a string encoding the secondary structure
# to a string of corresponding Martini types, taking the origin of the 
# secondary structure into account, and replacing termini if requested.
def ssClassification(ss,program="dssp"):      
                 
    # Translate dssp/pymol/gmx ss to Martini ss                                             
    ss  = ss.translate(sstt[program])                                                       
    # Separate the different secondary structure types                                      
    sep = dict([(i,ss.translate(sstd[i])) for i in sstd.keys()])       
    # Do type substitutions based on patterns                                               
    # If the ss type is not in the patterns lists, do not substitute                        
    # (use empty lists for substitutions) 

    typ = [ typesub(sep[i],patterns.get(i,[]),pattypes.get(i,[]))                           
            for i in sstd.keys()]                                                           
    # Translate all types to numerical values  
    typ = [ [ord(j) for j in list(i)] for i in typ ]                                        
    # Sum characters back to get a full typed sequence                                      
    typ = "".join([chr(sum(i)) for i in zip(*typ)])                                         
    # Return both the actual as well as the fully typed sequence                             
    return ss, typ


# Above shamelessly copied from martinize. Apologies...

ss_to_code = {'C': 1, # Free,
              'S': 2,
              'H': 3,
              '1': 4,
              '2': 5,
              '3': 6,
              'E': 7, # Extended
              'T': 8, # Turn
              'F': 9  # Fibril 
              }

ss_eq = list("CBHHHHBTF")

# Load things
P = PDBParser()
# P = PDBParser()
io = PDBIO()


# Parse PDB and run DSSP
pdbf_path = os.path.abspath(sys.argv[1])
aa_model = P.get_structure('aa_model', pdbf_path)

aa_model = determine_hbonds(aa_model)

# Convert to MARTINI types
# Assign by chain and build the cg structure already
structure_builder=StructureBuilder()
structure_builder.init_structure("cg_model")
structure_builder.init_seg(' ') # Empty SEGID

nbeads = 0
for model in aa_model:

    structure_builder.init_model(model.id)

    dssp = DSSP(model, pdbf_path)

    for chain in model:
        structure_builder.init_chain(chain.id)

        # Get SS information and translate it to MARTINI
        dssp_ss = []
        for residue in chain:
          if residue.id[0] != ' ':
            continue
          if "SS_DSSP" in residue.xtra:
            dssp_ss.append(residue.xtra["SS_DSSP"])
          else:
            dssp_ss.append('-')
        dssp_ss = ''.join(dssp_ss)

        #dssp_ss = ''.join([ residue.xtra["SS_DSSP"] for residue in chain if residue.id[0] == ' '])
        martini_ss, martini_types = ssClassification(dssp_ss)
        # exit()
        # aa_seq = ''.join([ protein_letters_3to1[residue.resname] for residue in chain if residue.id[0] == ' '])    

        tbl_cg_to_aa = []

        for residue, sstype in zip(chain.child_list, martini_types):

            if residue.id[0] != ' ': # filter HETATMS
              continue
            
            # Convert SS to bfactor code
            sscode = ss_to_code[sstype]
            #print sscode
            # Coarse grain residue
            # exit()
            # residue_restraints, beads = MARTINI(residue)
            residue_restraints, beads = mapcg(residue)
            structure_builder.init_residue(residue.resname, residue.id[0], residue.id[1], residue.id[2])
            # Populate residue
            for name,coord in beads:
                structure_builder.init_atom(name, coord, sscode, 1.00, " ", name, nbeads, ss_eq[int(sscode)-1])
                nbeads += 1
            # Save restraints
            tbl_cg_to_aa.extend(residue_restraints)

cg_model = structure_builder.get_structure()

# output sequence and ss information
# print "%s:\t" %chain.id, aa_seq
print "%s:\t" %chain.id, martini_types
print "%s:\t" %chain.id, ''.join(map(lambda x: str(ss_to_code[x]), martini_types))

# Write coarse grained structure
io.set_structure(cg_model)
io.save('%s_cg_dbg.pdb' %(pdbf_path[:-4]), write_end=1)
# Write Restraints
tbl_file = open('%s_cg_to_aa_dbg.tbl' %pdbf_path[:-4], 'w')
tbl_file.write('\n'.join(tbl_cg_to_aa))
tbl_file.close()
