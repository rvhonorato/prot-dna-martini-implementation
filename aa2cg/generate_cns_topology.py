def spl(x):                                                                   
    return x.split() 

# Charged types:
charges = {"Qd":1, "Qa":-1, "SQd":1, "SQa":-1, "RQd":1, "AQa":-1}                                                           #@#
bbcharges = {"BB1":-1}                                                                                                      #@#


#----+---------------------+
## A | BACKBONE PARAMETERS |
#----+---------------------+
#
# bbss  lists the one letter secondary structure code
# bbdef lists the corresponding default backbone beads
# bbtyp lists the corresponding residue specific backbone beads
#
# bbd   lists the structure specific backbone bond lengths
# bbkb  lists the corresponding bond force constants
#
# bba   lists the structure specific angles
# bbka  lists the corresponding angle force constants
#
# bbd   lists the structure specific dihedral angles
# bbkd  lists the corresponding force constants
#
# -=NOTE=- 
#  if the secondary structure types differ between bonded atoms
#  the bond is assigned the lowest corresponding force constant 
#
# -=NOTE=-
# if proline is anywhere in the helix, the BBB angle changes for 
# all residues
#

###############################################################################################
## BEADS ##                                                                         #                 
#                              F     E     H     1     2     3     T     S     C    # SS one letter   
bbdef    =    spl(" N0   Nda    N0    Nd    Na   Nda   Nda    P5    P5")  # Default beads   #@#
bbtyp    = {                                                                   #                 #@#
            "ALA": spl(" C5    N0    C5    N0    N0    N0    N0    P4    P4"), # ALA specific    #@#
            "PRO": spl(" C5    N0    C5    N0    Na    N0    N0    P4    P4"), # PRO specific    #@#
            "HYP": spl(" C5    N0    C5    N0    N0    N0    N0    P4    P4")  # HYP specific    #@#
}                                                                                   #                 #@#
## BONDS ##                                                                         #                 
bbldef   =             (.365, .350, .310, .310, .310, .310, .350, .350, .350)  # BB bond lengths #@#
bbkb     =             (1250, 1250, None, None, None, None, 1250, 1250, 1250)  # BB bond kB      #@#
bbltyp   = {}                                                                  #                 #@#
bbkbtyp  = {}                                                                  #                 #@#
## ANGLES ##                                                                        #                 
bbadef   =             ( 119.2,134,   96,   96,   96,   96,  100,  130,  127)  # BBB angles      #@#
bbka     =             ( 150,   25,  700,  700,  700,  700,   20,   20,   20)  # BBB angle kB    #@#
bbatyp   = {                                                                   #                 #@#
       "PRO":               ( 119.2,134,   98,   98,   98,   98,  100,  130,  127), # PRO specific    #@#
       "HYP":               ( 119.2,134,   98,   98,   98,   98,  100,  130,  127)  # PRO specific    #@#
}                                                                                   #                 #@#
bbkatyp  = {                                                                   #                 #@#
       "PRO":               ( 150,   25,  100,  100,  100,  100,   25,   25,   25), # PRO specific    #@#
       "HYP":               ( 150,   25,  100,  100,  100,  100,   25,   25,   25)  # PRO specific    #@#
}                                                                                   #                 #@#
## DIHEDRALS ##                                                                     #                 
bbddef   =             ( 90.7,   0, -120, -120, -120, -120)                    # BBBB dihedrals  #@#
bbkd     =             ( 100,   10,  400,  400,  400,  400)                    # BBBB kB         #@#
bbdmul   =             (   1,    1,    1,    1,    1,    1)                    # BBBB mltplcty   #@#
bbdtyp   = {}                                                                  #                 #@#
bbkdtyp  = {}                                                                  #                 #@#
                                                                                    #                 
###############################################################################################               

# Some Forcefields use the Ca position to position the BB-bead (me like!)
# martini 2.1 doesn't
ca2bb = False 

# BBS angle, equal for all ss types                                                         
# Connects BB(i-1),BB(i),SC(i), except for first residue: BB(i+1),BB(i),SC(i)               
#                 ANGLE   Ka                                                                
bbsangle =      [   100,  25]                                                               #@#

# Bonds for extended structures (more stable than using dihedrals)                          
#               LENGTH FORCE                                                                
ebonds   = {                                                                                #@#
       'short': [ .640, 2500],                                                              #@#
       'long' : [ .970, 2500]                                                               #@#
}                                                                                           #@#


#----+-----------------------+
## B | SIDE CHAIN PARAMETERS |
#----+-----------------------+

# To be compatible with Elnedyn, all parameters are explicitly defined, even if they are double.
sidechains = {
    #RES#   BEADS                       BONDS                                                   ANGLES                      DIHEDRALS
    #                                   BB-SC          SC-SC                                    BB-SC-SC  SC-SC-SC
    "TRP": [spl("SC4 SNd SC5 SC5"),[(0.300,5000)]+[(0.270,None) for i in range(5)],        [(210,50),(90,50),(90,50)], [(0,50),(0,200)]],
    "TYR": [spl("SC4 SC4 SP1"),    [(0.320,5000), (0.270,None), (0.270,None),(0.270,None)],[(150,50),(150,50)],        [(0,50)]],
    "PHE": [spl("SC5 SC5 SC5"),    [(0.310,7500), (0.270,None), (0.270,None),(0.270,None)],[(150,50),(150,50)],        [(0,50)]],
    "HIS": [spl("SC4 SP1 SP1"),    [(0.320,7500), (0.270,None), (0.270,None),(0.270,None)],[(150,50),(150,50)],        [(0,50)]],
    "HIH": [spl("SC4 SP1 SQd"),    [(0.320,7500), (0.270,None), (0.270,None),(0.270,None)],[(150,50),(150,50)],        [(0,50)]],
    "ARG": [spl("N0 Qd"),          [(0.330,5000), (0.340,5000)],                           [(180,25)]],
    "LYS": [spl("C3 Qd"),          [(0.330,5000), (0.280,5000)],                           [(180,25)]],
    "CYS": [spl("C5"),             [(0.310,7500)]],
    "ASP": [spl("Qa"),             [(0.320,7500)]],
    "GLU": [spl("Qa"),             [(0.400,5000)]],
    "ILE": [spl("AC1"),            [(0.310,None)]],
    "LEU": [spl("AC1"),            [(0.330,7500)]],
    "MET": [spl("C5"),             [(0.400,2500)]],
    "ASN": [spl("P5"),             [(0.320,5000)]],
    "PRO": [spl("C3"),             [(0.300,7500)]],
    "HYP": [spl("P1"),             [(0.300,7500)]],
    "GLN": [spl("P4"),             [(0.400,5000)]],
    "SER": [spl("P1"),             [(0.250,7500)]],
    "THR": [spl("P1"),             [(0.260,None)]],
    "VAL": [spl("AC2"),            [(0.265,None)]],
    "ALA": [],
    "GLY": [],
    }

# Not all (eg Elnedyn) forcefields use backbone-backbone-sidechain angles and BBBB-dihedrals.
UseBBSAngles          = True 
UseBBBBDihedrals      = True

# Martini 2.2p has polar and charged residues with seperate charges.
polar   = []
charged = []

# If masses or charged diverge from standard (45/72 and -/+1) they are defined here.
mass_charge = {
#RES   MASS               CHARGE
}

# Defines the connectivity between between beads
aa_connectivity = {
#RES       BONDS                                   ANGLES             DIHEDRALS              V-SITE
"TRP":     [[(0,1),(1,2),(1,3),(2,3),(2,4),(3,4)], [(0,1,2),(0,1,3)], [(0,2,3,1),(1,2,4,3)]],  
"TYR":     [[(0,1),(1,2),(1,3),(2,3)],             [(0,1,2),(0,1,3)], [(0,2,3,1)]], 
"PHE":     [[(0,1),(1,2),(1,3),(2,3)],             [(0,1,2),(0,1,3)], [(0,2,3,1)]],
"HIS":     [[(0,1),(1,2),(1,3),(2,3)],             [(0,1,2),(0,1,3)], [(0,2,3,1)]],
"HIH":     [[(0,1),(1,2),(1,3),(2,3)],             [(0,1,2),(0,1,3)], [(0,2,3,1)]],
"GLN":     [[(0,1)]],
"ASN":     [[(0,1)]],
"SER":     [[(0,1)]],
"THR":     [[(0,1)]],
"ARG":     [[(0,1),(1,2)],                         [(0,1,2)]],
"LYS":     [[(0,1),(1,2)],                         [(0,1,2)]],
"ASP":     [[(0,1)]],
"GLU":     [[(0,1)]],
"CYS":     [[(0,1)]],
"ILE":     [[(0,1)]],
"LEU":     [[(0,1)]],
"MET":     [[(0,1)]],
"PRO":     [[(0,1)]],
"HYP":     [[(0,1)]],
"VAL":     [[(0,1)]],
"ALA":     [],
"GLY":     [],
}

#----+----------------+
## C | DNA/RNA bases  |
#----+----------------+

# DNA BACKBONE PARAMETERS
dna_bb = {
    'atom'  : spl("Q0 SN0 SC2"),
    'bond'  : [(1,  0.360, 20000),          
               (1,  0.198, 80000),          
               (1,  0.353, 10000)],         
    'angle' : [(2,  110.0, 200),            
               (2,  102.0, 150),           
               (2,  106.0,  75)],           
    'dih'   : [(2,   95.0,  25),
               (1,  180.0,   2, 3),
               (9,   85.0,   2, 2,  9,  160.0,  2, 3)],
    'excl'  : [(), (), ()],
    'pair'  : [],
}
# DNA BACKBONE CONNECTIVITY
dna_con  = {
    'bond'  : [(0, 1),
               (1, 2),
               (2, 0)],
    'angle' : [(0, 1, 2),
               (1, 2, 0),
               (2, 0, 1)],
    'dih'   : [(0, 1, 2, 0),
               (1, 2, 0, 1),
               (2, 0, 1, 2)],
    'excl'  : [(0, 2), (1, 0),(2, 1)],
    'pair'  : [],
}

# RNA BACKBONE PARAMETERS
rna_bb = {
    'atom'  : spl("Q0 N0 C2"),
    'bond'  : [(0.120,5000),(0.220,5000),(0.320,5000)],
    'angle' : [(10.0, 100), (20.0, 100), (30.0, 100)],
    'dih'   : [(100, 10), (100, 10), (100, 10),],
    'excl'  : [],
}
# RNA BACKBONE CONNECTIVITY
rna_con  = {
    'bond'  : [(0,1),(1,2),(2,0)],
    'angle' : [(0,1,2),(1,2,0),(2,0,1)],
    'dih'   : [(0,1,2,0),(1,2,0,1),(2,0,1,2)],
    'excl'  : [],
}

# For bonds, angles, and dihedrals the first parameter should always 
# be the type. It is pretty annoying to check the connectivity from 
# elsewhere so we update these one base at a time.

# ADENINE
bases = {
    "DA": [spl("TN0 TA2 TA3 TNa"),                                      
    #     TYPE   EQUIL   OPTS TYPE   EQUIL   OPTS TYPE   EQUIL   OPTS
#                   [(1,  0.348, 20000), (1,  0.229,  None), (1,  0.266,  None),             # BONDS BB3-SC1 bond lengthened by 0.048 nm.
           [(1,  0.300, 30000), (1,  0.229,  None), (1,  0.266,  None),             # BONDS BB3-SC1 bond lengthened by 0.048 nm.
            (1,  0.326, 20000), (1,  0.288,  None), (1,  0.162,  None),],     
           [(2,   94.0,   250), (2,  160.0,   200), (2,  140.0,   200),             # ANGLES
            (1,   85.0,   200), (2,  158.0,   200), (1,  125.0,   200),
            (1,   74.0,   200), (1,   98.0,   200)],                           
           [(2,  -90.0,    20), (2, -116.0,   0.5), (2,   98.0,    15)],            # DIHEDRALS
           [],                                                                      # IMPROPERS 
           [],                                                                      # VSITES
           [(), (), (), (), (), (), (), (), (), (), (), (), (), ()],                # EXCLUSIONS
           []],                                                                     # PAIRS
    }
base_connectivity = {
    "DA": [[(2, 3),             (3, 4),             (4, 5),                         # BONDS
            (4, 6),             (5, 6),             (6, 3)],   
           [(1, 2, 3),          (2, 3, 4),          (2, 3, 6),                      # ANGLES
            (3, 4, 5),          (3, 2, 7),          (4, 3, 6),
            (4, 5, 6),          (5, 6, 3)], 
           [(0, 1, 2, 3),       (1, 2, 3, 4),       (1, 2, 3, 6),],                # DIHEDRALS        
           [],                                                                      # IMPROPERS
           [],                                                                      # VSITES
           [(0, 3),             (0, 4),             (0, 5),                         # EXCLUSIONS
            (0, 6),             (1, 3),             (1, 4),
            (1, 5),             (1, 6),             (2, 3),
            (2, 4),             (2, 5),             (2, 6),
            (3, 5),             (4, 6)],
           []],                                                                     # PAIRS                     
    }

# CYTOSINE
bases.update({
    "DC": [spl("TN0 TY2 TY3"),                                                     
    #     TYPE   EQUIL   OPTS TYPE   EQUIL   OPTS TYPE   EQUIL   OPTS
#                   [(1,  0.303, 20000), (1,  0.220,  None), (1,  0.285,  None),             # BONDS BB3-SC1 bond lenghtened by 0.033 nm.
           [(1,  0.270, 30000), (1,  0.220,  None), (1,  0.285,  None),             # BONDS BB3-SC1 bond lenghtened by 0.033 nm.
            (1,  0.268,  None),],
           [(2,   95.0,   210), (2,   95.0,   300), (1,  150.0,   500),             # ANGLES
            (1,  180.0,    30), (1,   61.0,   200), (1,   71.0,   200), 
            (1,   47.0,   200)],
           [(2,  -78.0,    25), (2,  -90.0,    20), (2, -142.0,    50)],            # DIHEDRALS
           #[(2,  -78.0,    25), (2, -108.0,    10), (2,   40.0,    15)],            # DIHEDRALS
           [],                                                                      # IMPROPERS
           [],                                                                      # VSITES
           [(), (), (), (), (), (), (), (), ()],                                    # EXCLUSIONS
           []],                                                                     # PAIRS                     
})
base_connectivity.update({
    "DC": [[(2, 3),           (3, 4),             (4, 5),                         # BONDS
            (5, 3)],
           [(1, 2, 3),        (2, 3, 4),          (1, 3, 5),                      # ANGLES
            (3, 2, 6),        (3, 4, 5),          (4, 3, 5),
            (4, 5, 3)],
           [(0, 1, 2, 3),     (1, 2, 3, 4),       (2, 1, 3, 5)],                  # DIHEDRALS
           [],                                                                    # IMPROPERS
           [],                                                                    # VSITES
           [(0, 3),             (0, 4),             (0, 5),                         # EXCLUSIONS
            (1, 3),             (1, 4),             (1, 5),             
            (2, 3),             (2, 4),             (2, 5)],                                           
           []],                                                                     # PAIRS                     
})

# GUANINE
bases.update({
    "DG": [spl("TN0 TG2 TG3 TNa"),
    #     TYPE   EQUIL   OPTS TYPE   EQUIL   OPTS TYPE   EQUIL   OPTS
#                   [(1,  0.353, 20000), (1,  0.295,  None), (1,  0.295,  None),             # BONDS BB3-SC1 bond lengthened by 0.053 nm.
           [(1,  0.300, 30000), (1,  0.295,  None), (1,  0.295,  None),             # BONDS BB3-SC1 bond lengthened by 0.053 nm.
            (1,  0.389, 20000), (1,  0.285,  None), (1,  0.161,  None),],     
           [(2,   94.5,   250), (2,  137.0,   300), (2,  130.0,   250),             # ANGLES
            (1,   69.5,   200), (2,  157.0,   150), (1,  125.0,   200),
            (1,   84.0,   200), (1,   94.0,   200)],                           
           [(2,  -90.0,    20), (2, -117.0,     1), (2,   92.0,    15)],            # DIHEDRALS  
           [],                                                                      # IMPROPERS 
           [],                                                                      # VSITES
           [(), (), (), (), (), (), (), (), (), (), (), (), (), ()],                # EXCLUSIONS
           []],                                                                     # PAIRS                     
})
base_connectivity.update({
    "DG": [[(2, 3),             (3, 4),             (4, 5),                         # BONDS
            (4, 6),             (5, 6),             (6, 3)],
           [(1, 2, 3),          (2, 3, 4),          (2, 3, 6),                      # ANGLES
            (3, 4, 5),          (3, 2, 7),          (4, 3, 6), 
            (4, 5, 6),          (5, 6, 3)],
           [(0, 1, 2, 3),       (1, 2, 3, 4),       (1, 2, 3, 6),],                 # DIHEDRALS        
           [],                                                                      # IMPROPERS
           [],                                                                      # VSITES
           [(0, 3),             (0, 4),             (0, 5),                         # EXCLUSIONS
            (0, 6),             (1, 3),             (1, 4),
            (1, 5),             (1, 6),             (2, 3),
            (2, 4),             (2, 5),             (2, 6),
            (3, 5),             (4, 6)],                                           
           []],                                                                     # PAIRS                     
})

# THYMINE
bases.update({
    "DT": [spl("TN0 TT2 TT3"),
    #     TYPE   EQUIL   OPTS TYPE   EQUIL   OPTS TYPE   EQUIL   OPTS
#                   [(1,  0.326, 20000), (1,  0.217,  None), (1,  0.322,  None),             # BONDS BB3-SC1 bond lengthened by 0.056 nm.
           [(1,  0.270, 30000), (1,  0.217,  None), (1,  0.322,  None),             # BONDS BB3-SC1 bond lengthened by 0.056 nm.
            (1,  0.265,  None),],
           [(2,   92.0,   220), (2,  107.0,   300), (1,  145.0,   400),             # ANGLES
            (1,  180.0,    30), (1,   55.0,   100), (1,   83.0,   100),
            (1,   42.0,   100)],
           [(2,  -75.0,    40), (2, -110.0,    15), (2, -145.0,    65)],            # DIHEDRALS
           [],                                                                      # IMPROPERS
           [],                                                                      # VSITES
           [(), (), (), (), (), (), (), (), ()],                                    # EXCLUSIONS
           []],                                                                     # PAIRS                     
})
base_connectivity.update({
    "DT": [[(2, 3),           (3, 4),             (4, 5),                         # BONDS
            (5, 3)],
           [(1, 2, 3),        (2, 3, 4),          (1, 3, 5),                      # ANGLES
            (3, 2, 6),        (3, 4, 5),          (4, 3, 5), 
            (4, 5, 3)],
           [(0, 1, 2, 3),     (1, 2, 3, 4),       (2, 1, 3, 5)],                  # DIHEDRALS
           [],                                                                    # IMPROPERS
           [],                                                                    # VSITES
           [(0, 3),             (0, 4),             (0, 5),                         # EXCLUSIONS
            (1, 3),             (1, 4),             (1, 5),             
            (2, 3),             (2, 4),             (2, 5)],                                           
           []],                                                                     # PAIRS                     
})


#----+----------------+
## D | SPECIAL BONDS  |
#----+----------------+

special = {
    # Used for sulfur bridges
    # ATOM 1         ATOM 2          BOND LENGTH   FORCE CONSTANT
    (("SC1","CYS"), ("SC1","CYS")):     (0.39,         5000),
    }

#=========================================================================#
# start here


