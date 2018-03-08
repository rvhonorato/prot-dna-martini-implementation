class martini22dna:
    def __init__(self):

        # parameters are defined here for the following (protein) forcefields:
        self.name = 'martini22dna'
        
        # Charged types:
        self.charges = {"Qd":1, "Qa":-1, "SQd":1, "SQa":-1, "RQd":1, "AQa":-1}                                                           #@#
        self.bbcharges = {"BB1":-1}                                                                                                      #@#
        
        
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
        self.bbdef    =    spl(" N0   Nda    N0    Nd    Na   Nda   Nda    P5    P5")  # Default beads   #@#
        self.bbtyp    = {                                                                   #                 #@#
                    "ALA": spl(" C5    N0    C5    N0    N0    N0    N0    P4    P4"), # ALA specific    #@#
                    "PRO": spl(" C5    N0    C5    N0    Na    N0    N0    P4    P4"), # PRO specific    #@#
                    "HYP": spl(" C5    N0    C5    N0    N0    N0    N0    P4    P4")  # HYP specific    #@#
        }                                                                                   #                 #@#
        ## BONDS ##                                                                         #                 
        self.bbldef   =             (.365, .350, .310, .310, .310, .310, .350, .350, .350)  # BB bond lengths #@#
        self.bbkb     =             (1250, 1250, None, None, None, None, 1250, 1250, 1250)  # BB bond kB      #@#
        self.bbltyp   = {}                                                                  #                 #@#
        self.bbkbtyp  = {}                                                                  #                 #@#
        ## ANGLES ##                                                                        #                 
        self.bbadef   =             ( 119.2,134,   96,   96,   96,   96,  100,  130,  127)  # BBB angles      #@#
        self.bbka     =             ( 150,   25,  700,  700,  700,  700,   20,   20,   20)  # BBB angle kB    #@#
        self.bbatyp   = {                                                                   #                 #@#
               "PRO":               ( 119.2,134,   98,   98,   98,   98,  100,  130,  127), # PRO specific    #@#
               "HYP":               ( 119.2,134,   98,   98,   98,   98,  100,  130,  127)  # PRO specific    #@#
        }                                                                                   #                 #@#
        self.bbkatyp  = {                                                                   #                 #@#
               "PRO":               ( 150,   25,  100,  100,  100,  100,   25,   25,   25), # PRO specific    #@#
               "HYP":               ( 150,   25,  100,  100,  100,  100,   25,   25,   25)  # PRO specific    #@#
        }                                                                                   #                 #@#
        ## DIHEDRALS ##                                                                     #                 
        self.bbddef   =             ( 90.7,   0, -120, -120, -120, -120)                    # BBBB dihedrals  #@#
        self.bbkd     =             ( 100,   10,  400,  400,  400,  400)                    # BBBB kB         #@#
        self.bbdmul   =             (   1,    1,    1,    1,    1,    1)                    # BBBB mltplcty   #@#
        self.bbdtyp   = {}                                                                  #                 #@#
        self.bbkdtyp  = {}                                                                  #                 #@#
                                                                                            #                 
        ###############################################################################################               
        
        # Some Forcefields use the Ca position to position the BB-bead (me like!)
        # martini 2.1 doesn't
        self.ca2bb = False 
        
        # BBS angle, equal for all ss types                                                         
        # Connects BB(i-1),BB(i),SC(i), except for first residue: BB(i+1),BB(i),SC(i)               
        #                 ANGLE   Ka                                                                
        self.bbsangle =      [   100,  25]                                                               #@#
        
        # Bonds for extended structures (more stable than using dihedrals)                          
        #               LENGTH FORCE                                                                
        self.ebonds   = {                                                                                #@#
               'short': [ .640, 2500],                                                              #@#
               'long' : [ .970, 2500]                                                               #@#
        }                                                                                           #@#
        
        
        #----+-----------------------+
        ## B | SIDE CHAIN PARAMETERS |
        #----+-----------------------+
        
        # To be compatible with Elnedyn, all parameters are explicitly defined, even if they are double.
        self.sidechains = {
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
        self.UseBBSAngles          = True 
        self.UseBBBBDihedrals      = True

        # Martini 2.2p has polar and charged residues with seperate charges.
        self.polar   = []
        self.charged = []

        # If masses or charged diverge from standard (45/72 and -/+1) they are defined here.
        self.mass_charge = {
        #RES   MASS               CHARGE
        }

        # Defines the connectivity between between beads
        self.aa_connectivity = {
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
        self.dna_bb = {
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
        self.dna_con  = {
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
        self.rna_bb = {
            'atom'  : spl("Q0 N0 C2"),
            'bond'  : [(0.120,5000),(0.220,5000),(0.320,5000)],
            'angle' : [(10.0, 100), (20.0, 100), (30.0, 100)],
            'dih'   : [(100, 10), (100, 10), (100, 10),],
            'excl'  : [],
        }
        # RNA BACKBONE CONNECTIVITY
        self.rna_con  = {
            'bond'  : [(0,1),(1,2),(2,0)],
            'angle' : [(0,1,2),(1,2,0),(2,0,1)],
            'dih'   : [(0,1,2,0),(1,2,0,1),(2,0,1,2)],
            'excl'  : [],
        }

        # For bonds, angles, and dihedrals the first parameter should always 
        # be the type. It is pretty annoying to check the connectivity from 
        # elsewhere so we update these one base at a time.

        # ADENINE
        self.bases = {
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
        self.base_connectivity = {
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
        self.bases.update({
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
        self.base_connectivity.update({
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
        self.bases.update({
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
        self.base_connectivity.update({
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
        self.bases.update({
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
        self.base_connectivity.update({
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
        
        self.special = {
            # Used for sulfur bridges
            # ATOM 1         ATOM 2          BOND LENGTH   FORCE CONSTANT
            (("SC1","CYS"), ("SC1","CYS")):     (0.39,         5000),
            }
        
        # By default use an elastic network
        self.ElasticNetwork = False 

        # Elastic networks bond shouldn't lead to exclusions (type 6) 
        # But Elnedyn has been parametrized with type 1.
        self.EBondType = 6
        
        #----+----------------+
        ## D | INTERNAL STUFF |
        #----+----------------+
        
        
        ## BACKBONE BEAD TYPE ##                                                                    
        # Dictionary of default bead types (*D)                                                     
        self.bbBeadDictD  = hash(bbss,self.bbdef)                                                             
        # Dictionary of dictionaries of types for specific residues (*S)                            
        self.bbBeadDictS  = dict([(i,hash(bbss,self.bbtyp[i])) for i in self.bbtyp.keys()])                        

        # combine the connectivity records for different molecule types
        self.connectivity = dict(self.base_connectivity.items() + self.aa_connectivity.items())
        # XXX No need to do that, let's just use separate for DNA for now
        
        ## BB BOND TYPE ##                                                                          
        # Dictionary of default abond types (*D)                                                    
        self.bbBondDictD = hash(bbss,zip(self.bbldef,self.bbkb))                                                   
        # Dictionary of dictionaries for specific types (*S)                                        
        self.bbBondDictS = dict([(i,hash(bbss,zip(self.bbltyp[i],self.bbkbtyp[i]))) for i in self.bbltyp.keys()])       
        # This is tricky to read, but it gives the right bondlength/force constant
        
        ## BBB ANGLE TYPE ##                                                                        
        # Dictionary of default angle types (*D)                                                    
        self.bbAngleDictD = hash(bbss,zip(self.bbadef,self.bbka))                                                  
        # Dictionary of dictionaries for specific types (*S)                                        
        self.bbAngleDictS = dict([(i,hash(bbss,zip(self.bbatyp[i],self.bbkatyp[i]))) for i in self.bbatyp.keys()])      
                    
        ## BBBB DIHEDRAL TYPE ##                                                                    
        # Dictionary of default dihedral types (*D)                                                 
        self.bbDihedDictD = hash(bbss,zip(self.bbddef,self.bbkd,self.bbdmul))                                           
        # Dictionary of dictionaries for specific types (*S)                                        
        self.bbDihedDictS = dict([(i,hash(bbss,zip(self.bbdtyp[i],self.bbkdtyp[i]))) for i in self.bbdtyp.keys()])      

        ## DNA DICTIONARIES ##
        # Dictionary for the connectivities and parameters of bonds between DNA backbone beads
        self.dnaBbBondDictC = dict(zip(self.dna_con['bond'],self.dna_bb['bond']))
        # Dictionary for the connectivities and parameters of angles between DNA backbone beads
        self.dnaBbAngleDictC = dict(zip(self.dna_con['angle'],self.dna_bb['angle']))
        # Dictionary for the connectivities and parameters of dihedrals between DNA backbone beads
        self.dnaBbDihDictC = dict(zip(self.dna_con['dih'],self.dna_bb['dih']))
        # Dictionary for exclusions for DNA backbone beads
        self.dnaBbExclDictC = dict(zip(self.dna_con['excl'],self.dna_bb['excl']))
        # Dictionary for pairs for DNA backbone beads
        self.dnaBbPairDictC = dict(zip(self.dna_con['pair'],self.dna_bb['pair']))

        ## RNA DICTIONARIES ##
        # Dictionary for the connectivities and parameters of bonds between RNA backbone beads
        self.rnaBbBondDictC = dict(zip(self.rna_con['bond'],self.rna_bb['bond']))
        # Dictionary for the connectivities and parameters of angles between rna backbone beads
        self.rnaBbAngleDictC = dict(zip(self.rna_con['angle'],self.rna_bb['angle']))
        # Dictionary for the connectivities and parameters of dihedrals between rna backbone beads
        self.rnaBbDihDictC = dict(zip(self.rna_con['dih'],self.rna_bb['dih']))
        # Dictionary for exclusions for RNA backbone beads
        self.rnaBbExclDictC = dict(zip(self.rna_con['excl'],self.rna_bb['excl']))
        
        
    # The following function returns the backbone bead for a given residue and                   
    # secondary structure type.                                                                 
    # 1. Check if the residue is DNA/RNA and return the whole backbone for those
    # 2. Look up the proper dictionary for the residue                                          
    # 3. Get the proper type from it for the secondary structure                                
    # If the residue is not in the dictionary of specials, use the default                      
    # If the secondary structure is not listed (in the residue specific                         
    # dictionary) revert to the default.                                                        
    def bbGetBead(self,r1,ss="C"):                                                               
        if r1 in dnares3:
            return self.dna_bb['atom']
        elif r1 in rnares3:
            return self.rna_bb['atom']
        else:
            return self.bbBeadDictS.get(r1,self.bbBeadDictD).get(ss,self.bbBeadDictD.get(ss))                      
    
    def bbGetBond(self,r,ca,ss):
        # Retrieve parameters for each residue from tables defined above
        # Check is it DNA residue
        if r[0] in dnares3:
            return ca in self.dnaBbBondDictC.keys() and self.dnaBbBondDictC[ca] or None
        # RNA is not implemented properly yet
        elif r[0] in rnares3:
            return ca in self.rnaBbBondDictC.keys() and self.rnaBbBondDictC[ca] or None
        # If it's protein
        else:
            b1 = self.bbBondDictS.get(r[0],self.bbBondDictD).get(ss[0],self.bbBondDictD.get(ss[0]))
            b2 = self.bbBondDictS.get(r[1],self.bbBondDictD).get(ss[1],self.bbBondDictD.get(ss[1]))
            # Determine which parameters to use for the bond
            return ( (b1[0]+b2[0])/2, min(b1[1],b2[1]) )
    
    def bbGetAngle(self,r,ca,ss):
        # Check is it DNA residue
        if r[0] in dnares3:
            return ca in self.dnaBbAngleDictC.keys() and self.dnaBbAngleDictC[ca] or None
        # RNA is not implemented properly yet
        elif r[0] in rnares3:
            return ca in self.rnaBbAngleDictC.keys() and self.rnaBbAngleDictC[ca] or None
        # For protein
        else:
            # PRO in helices is dominant
            if r[1] == "PRO" and ss[1] in "H123":
                return self.bbAngleDictS["PRO"].get(ss[1])
            else:
                # Retrieve parameters for each residue from table defined above
                a = [ self.bbAngleDictS.get(r[0],self.bbAngleDictD).get(ss[0],self.bbAngleDictD.get(ss[0])),
                      self.bbAngleDictS.get(r[1],self.bbAngleDictD).get(ss[1],self.bbAngleDictD.get(ss[1])),
                      self.bbAngleDictS.get(r[2],self.bbAngleDictD).get(ss[2],self.bbAngleDictD.get(ss[2])) ]
                # Sort according to force constant
                a.sort(key=lambda i: (i[1],i[0]))
                # This selects the set with the smallest force constant and the smallest angle
                return a[0]

    def bbGetExclusion(self,r,ca,ss):
        if r[0] in dnares3:
            return ca in self.dnaBbExclDictC.keys() and ' ' or None
        # RNA is not implemented properly yet
        elif r[0] in rnares3:
            return ca in self.rnaBbExclDictC.keys() and ' ' or None
        else:
            return None

    def bbGetPair(self,r,ca,ss):
        if r[0] in dnares3:
            return ca in self.dnaBbPairDictC.keys() and ' ' or None
        # RNA is not implemented properly yet
        elif r[0] in rnares3:
            return ca in self.rnaBbPairDictC.keys() and ' ' or None
        else:
            return None

    def bbGetDihedral(self,r,ca,ss):
        # Retrieve parameters for each residue from table defined above
        # Check is it DNA residue
        if r[0] in dnares3:
            return ca in self.dnaBbDihDictC.keys() and self.dnaBbDihDictC[ca] or None
        # RNA is not implemented properly yet
        elif r[0] in rnares3:
            return ca in self.rnaBbDihDictC.keys() and self.rnaBbDihDictC[ca] or None
        # Apparently protein has none currently

    def getCharge(self,atype,aname):
        return self.charges.get(atype,self.bbcharges.get(aname,0))
        
    def messages(self):
        '''Prints any force-field specific logging messages.'''
        import logging
        logging.warning('#####################################################################################')
        logging.warning('This is a version of martinize for DNA and should NOT be used for proteins.')
        logging.warning('#####################################################################################')
        pass


# Split a string                                                              
def spl(x):                                                                   
    return x.split()                                                          


# Split each argument in a list                                               
def nsplit(*x):                                                               
    return [i.split() for i in x]                                             


# Make a dictionary from two lists                                            
def hash(x,y):                                                                
    return dict(zip(x,y))                                                     


# Function to reformat pattern strings                                        
def pat(x,c="."):                                                             
    return x.replace(c,"\x00").split()                                        


# Function to generate formatted strings according to the argument type       
def formatString(i):                                                          
    if type(i) == str:                                                        
        return i                                                              
    if type(i) == int:                                                        
        return "%5d"%i                                                        
    if type(i) == float and 0<abs(i)<1e-5:                                                      
        return "%2.1e"%i                                                      
    elif type(i) == float:                                                      
        return "%8.5f"%i                                                      
    else:                                                                     
        return str(i)           

import logging,os,sys
import subprocess as subp

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

    
#----+----------+
## C | INTERNAL |
#----+----------+




#============================================================================================================#
#============================================================================================================#
#============================================================================================================#
#============================================================================================================#

# extract information from this class
m = martini22dna()


# atom names
atom_name_dic = {0:'nB0', 1:'nB1',2:'nB2',3:'S0',4:'S1',5:'S2',6:'S3',7:'S4',8:'S5',9:'S6',10:'S7',11:'S8',12:'S9'}

reference_file = 'haddock-martini-dna-bead-reference_4top.csv'
bead_dic = dict([(l.split(',')[0],l.split(',')[1].split('\n')[0].split('\r')[0]) for l in open(reference_file).readlines()[1:]])

# for nuc in m.bases():

nuc = 'DG'

# m.bases['DT'][0] # beads
beads = dict([(i, b) for i, b in enumerate(m.dna_bb['atom'] + m.bases[nuc][0])]) 
beads[max(beads.keys())+1] = m.dna_bb['atom'][0] + '*'

if not 'h' in nuc:
    bead_type_key = nuc[-1].lower()

# get dna bb bond info
bb_bonds = []
for p in m.dna_con['bond']:
    #
    atomA = atom_name_dic[p[0]]
    atomB = atom_name_dic[p[1]]
    #
    bb_bonds.append('  BOND %s %s' %  (atomA, atomB))

# get dna bb angle info
bb_angles = []
angles_param = []
for i, p in enumerate(m.dna_con['angle']):
    #
    atomA = atom_name_dic[p[0]]
    atomB = atom_name_dic[p[1]]
    atomC = atom_name_dic[p[2]]
    #
    bb_angles.append('  ANGLE %s %s %s' % (atomA, atomB, atomC))
    #
    angle_type, equil, opts = m.dna_bb['angle'][i]
    #
    # print m_beadA, m_beadB, m_beadC, angle_type, equil, opts
    m_beadA = beads[p[0]]
    m_beadB = beads[p[1]]
    m_beadC = beads[p[2]]
    h_beadA = [e for e in bead_dic if bead_dic[e] == m_beadA and bead_type_key in e[0]][0]
    h_beadB = [e for e in bead_dic if bead_dic[e] == m_beadB and bead_type_key in e[0]][0]
    h_beadC = [e for e in bead_dic if bead_dic[e] == m_beadC and bead_type_key in e[0]][0]
    #
    angles_param.append('ANGLe %s %s %s %.3f %i' % (h_beadA, h_beadB, h_beadC, equil, opts))

# dihedrals
bb_dih_angles = []
dih_param = []
for i, p in enumerate(m.dna_con['dih']):
    #
    atomA = atom_name_dic[p[0]]
    atomB = atom_name_dic[p[1]]
    atomC = atom_name_dic[p[2]]
    atomD = atom_name_dic[p[3]]
    #
    bb_dih_angles.append('  DIHEdral %s %s %s %s' % (atomA, atomB, atomC, atomD))
    #
    angle_type, equil, opts = m.dna_bb['dih'][i]
    #
    # print m_beadA, m_beadB, m_beadC, angle_type, equil, opts
    m_beadA = beads[p[0]]
    m_beadB = beads[p[1]]
    m_beadC = beads[p[2]]
    m_beadD = beads[p[3]]
    #
    h_beadA = [e for e in bead_dic if bead_dic[e] == m_beadA and bead_type_key in e[0]][0]
    h_beadB = [e for e in bead_dic if bead_dic[e] == m_beadB and bead_type_key in e[0]][0]
    h_beadC = [e for e in bead_dic if bead_dic[e] == m_beadC and bead_type_key in e[0]][0]
    h_beadD = [e for e in bead_dic if bead_dic[e] == m_beadD and bead_type_key in e[0]][0]
    #
    dih_param.append('DIHEdral %s %s %s %s %.3f %i' % (h_beadA, h_beadB, h_beadC, h_beadD, equil, opts))






bonds = bb_bonds
for i, p in enumerate(m.base_connectivity[nuc][0]):
    #
    # topology
    # m_beadA = beads[p[0]]
    # m_beadB = beads[p[1]]
    #
    atomA = atom_name_dic[p[0]]
    atomB = atom_name_dic[p[1]]
    #
    bonds.append('  BOND %s %s' % (atomA, atomB))

angles = bb_angles
angles_param = angles_param_bb
for i, p in enumerate(m.base_connectivity[nuc][1]):
    #
    m_beadA = beads[p[0]]
    m_beadB = beads[p[1]]
    m_beadC = beads[p[2]]
    #
    atomA = atom_name_dic[p[0]]
    atomB = atom_name_dic[p[1]]
    atomC = atom_name_dic[p[2]]
    if any('*' in b for b in [m_beadA, m_beadB, m_beadC]): 
        # # special case, investigate
        # print '*******  ANGLE', m_beadA, m_beadB, m_beadC
        continue
    # 
    angles.append('  ANGLE %s %s %s' % (atomA, atomB, atomC))
    #
    # parameters
    h_beadA = [e for e in bead_dic if bead_dic[e] == m_beadA and bead_type_key in e[0]][0]
    h_beadB = [e for e in bead_dic if bead_dic[e] == m_beadB and bead_type_key in e[0]][0]
    h_beadC = [e for e in bead_dic if bead_dic[e] == m_beadC and bead_type_key in e[0]][0]
    #
    angle_type, equil, opts = m.bases[nuc][2][i]
    #
    print m_beadA, m_beadB, m_beadC, angle_type, equil, opts
    angles_param.append('ANGLe %s %s %s %.3f %i' % (h_beadA, h_beadB, h_beadC, equil, opts))


# dihedrals
for p in m.base_connectivity['DA'][2]:
    # try:
    m_beadA = beads[p[0]]
    m_beadB = beads[p[1]]
    m_beadC = beads[p[2]]
    m_beadD = beads[p[3]]
    # except:
        # continue
    #
    h_beadA = [e for e in bead_dic if bead_dic[e] == m_beadA and bead_type_key in e[0]][0]
    h_beadB = [e for e in bead_dic if bead_dic[e] == m_beadB and bead_type_key in e[0]][0]
    h_beadC = [e for e in bead_dic if bead_dic[e] == m_beadC and bead_type_key in e[0]][0]
    h_beadD = [e for e in bead_dic if bead_dic[e] == m_beadD and bead_type_key in e[0]][0]
    #
    # print '  DIHEdral', m_beadA, m_beadB, m_beadC, m_beadD
    print '  DIHEdral', h_beadA, h_beadB, h_beadC, h_beadD

# no impropers


# any(substring in string for substring in substring_list)




m.bases['DA'][4] # impropers
m.bases['DA'][5] # exclusions
m.bases['DA'][6] # pairs
