!/usr/bin/env python

"""
Uses Biopython to parse the structure and DSSP output.
Uses pieces of the martinize-1.1.py script to convert the SS types

Outputs a coarse grained pdb file (*_ss.pdb) with assigned bfactors.
Outputs a tbl file to map the beads to the atoms they represent.

Updates
 - Updated python version to 2.6 to support isdisjoint() set method in DSSP.py (JR Apr 2012)
 - Residues that DSSP can't handle (incomplete backbone f ex) treated as coil  (JR Apr 2012)

"""
import os
import sys
import warnings

try:
  from Bio.PDB import PDBParser
  from Bio.PDB import PDBIO
  from Bio.PDB.DSSP import DSSP
  from Bio.PDB import Entity
  from Bio.Data.SCOPData import protein_letters_3to1 as to_one_letter_code 
  from Bio.Data.IUPACData import protein_letters_1to3 as to_three_letter_code
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

## Coarse Graining

def MARTINI(aares, user_chain):
    """
    Reduces complexity of protein residue to the MARTINI coarse grained model:
    CA, O, Bead(s) in specific atom location.
    
    Reference:
    Monticelli et al. The MARTINI coarse-grained force field: extension to proteins. 
    J. Chem. Theory Comput. (2008) vol. 4 (5) pp. 819-834
    
    Martinize Script from Tserk Wassenaar
    """
    
    bb = "CA C N O "    
    cg_mapping = {      "ALA":  [bb + "CB"],
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
                        "ASN":  [bb, "CB CG ND1 ND2 OD1 OD2"],
                        "PRO":  [bb, "CB CG CD"],
                        "GLN":  [bb, "CB CG CD OE1 OE2 NE1 NE2"],
                        "ARG":  [bb, "CB CG CD","NE CZ NH1 NH2"],    
                        "SER":  [bb, "CB OG"],
                        "THR":  [bb, "CB OG1 CG2"],
                        "VAL":  [bb, "CB CG1 CG2"],
                        "TRP":  [bb, "CB CG CD2","CD1 NE1 CE2","CE3 CZ3","CZ2 CH2"],
                        "TYR":  [bb, "CB CG CD1","CD2 CE2","CE1 CZ OH"],
                        }
                        
    cg_to_aa_restraints = []
    beads = []
    bead_names = [" BB", " SC1", " SC2", " SC3", " SC4"] # Space bc of IO issues.
    resn = aares.resname
    segid = aares.segid.strip()
    if not segid:
        segid = user_chain
    resi = aares.id[1]
    
    try:
        atom_groups = cg_mapping[resn]
    except KeyError:
        raise ValueError("Residue %s not recognized" %resn)
        
    # delete and replace side chain atoms
    for index, centroid in enumerate(atom_groups):
        bname = bead_names[index]

        # Get as many atoms as possible..
        atoms = [aares[atom] for atom in centroid.split() if atom in aares.child_dict]
        if not atoms:
            resi = aares.id[1]
            chain = aares.parent.id
            sys.stderr.write('Residue %(resn)s%(resi)s of chain %(chain)s cannot be processed: missing atoms (%(centroid)s)\n' %locals())
            #sys.exit(1)
            continue
        # Get center of mass of bead based on the position and mass of atoms
        bcom = center_of_mass(atoms)
        beads.append((bname, bcom))

        # Output restraint pairs for CG to AA conversion
        cg_to_aa_restraints.append("assign (segid %sCG and resid %i and name %s) (segid %s and resid %i and (name %s)) 0 0 0" %(segid, resi, bname.strip(), segid, resi, ' or name '.join([a.name for a in atoms])))

    return (cg_to_aa_restraints, beads)

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


###### MAIN CODE ######

warnings.simplefilter('ignore') # Silence PDB Parser warnings

# Load things
P = PDBParser()
io = PDBIO()


# Parse PDB and run DSSP
pdbf_path = os.path.abspath(sys.argv[1])
pdb_chain = sys.argv[2]

aa_model = P.get_structure('aa_model', pdbf_path)

# Standardize aminoacid names
# Ugly hack, have to read, change, rewrite, and re-read PDB..
for residue in aa_model.get_residues():
    cur_name = residue.resname
    std_name = to_three_letter_code[to_one_letter_code[cur_name]].upper()
    residue.resname = std_name

io.set_structure(aa_model)
temp_pdbf_path = '%s-temp.pdb' %os.path.basename(pdbf_path)[:-4]
io.save(temp_pdbf_path)

# Convert to MARTINI types
# Assign by chain and build the cg structure already
structure_builder=StructureBuilder()
structure_builder.init_structure("cg_model")
structure_builder.init_seg(' ') # Empty SEGID

nbeads = 0
for model in aa_model:
    structure_builder.init_model(model.id)
    
    # Run DSSP
    dssp = DSSP(model, temp_pdbf_path)

    # CG Model
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
        aa_seq = ''.join([ to_one_letter_code[residue.resname] for residue in chain if residue.id[0] == ' '])    

        tbl_cg_to_aa = []

        for residue, sstype in zip(chain.child_list, martini_types):

            if residue.id[0] != ' ': # filter HETATMS
              continue
            
            # Convert SS to bfactor code
            sscode = ss_to_code[sstype]
            # Coarse grain residue
            residue_restraints, beads = MARTINI(residue, pdb_chain)
            structure_builder.init_residue(residue.resname, residue.id[0], residue.id[1], residue.id[2])
            # Populate residue
            for name,coord in beads:
                structure_builder.init_atom(name, coord, sscode, 1.00, " ", name, nbeads, "C")
                nbeads += 1
            # Save restraints
            tbl_cg_to_aa.extend(residue_restraints)

cg_model = structure_builder.get_structure()

# output sequence and ss information
print "%s:\t" %chain.id, aa_seq
print "%s:\t" %chain.id, martini_types
print "%s:\t" %chain.id, ''.join(map(lambda x: str(ss_to_code[x]), martini_types))

# Write coarse grained structure
io.set_structure(cg_model)
io.save('%s_cg.pdb' %(pdbf_path[:-4]), write_end=1)
# Write Restraints
tbl_file = open('%s_cg_to_aa.tbl' %pdbf_path[:-4], 'w')
tbl_file.write('\n'.join(tbl_cg_to_aa)+'\n')
tbl_file.close()

# Remove temporary file
os.remove(temp_pdbf_path)
