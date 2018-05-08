# Based on data extracted from the martinize-dna+py script, automatically generate a topology file for CNS
#
# This script has the potential to also generate angles, dihedrals and exclusion parameters
#  <09032018 Waiting on confirmation from the MARTINI team>
#


######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
#
#
# INFORMATION COPIED FROM THE martinize-dna.py
#
#
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

# Split a string                                                              
def spl(x):                                                                   
	return x.split()    

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
# rna_bb = {
# 	'atom'  : spl("Q0 N0 C2"),
# 	'bond'  : [(0.120,5000),(0.220,5000),(0.320,5000)],
# 	'angle' : [(10.0, 100), (20.0, 100), (30.0, 100)],
# 	'dih'   : [(100, 10), (100, 10), (100, 10),],
# 	'excl'  : [],
# }
# RNA BACKBONE CONNECTIVITY
# rna_con  = {
# 	'bond'  : [(0,1),(1,2),(2,0)],
# 	'angle' : [(0,1,2),(1,2,0),(2,0,1)],
# 	'dih'   : [(0,1,2,0),(1,2,0,1),(2,0,1,2)],
# 	'excl'  : [],
# }

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

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

#========================================================================================================================#

# Read a csv reference file that tells which haddock bead correlates to which martini bead
reference_file = 'haddock-martini-bead-reference_4top.csv'
bead_dic = dict([(l.split(',')[0],l.split(',')[1].split('\n')[0].split('\r')[0]) for l in open(reference_file).readlines()])

# define atom names (these are the ones you will see on the PDB)
atom_name_dic = {0:'nB0', 1:'nB1',2:'nB2',3:'S0',4:'S1',5:'S2',6:'S3',7:'S4',8:'S5',9:'S6',10:'S7',11:'S8',12:'S9'}

# produce a topology file containing the following nucleotides
base_list = [
			#
			# standard nucleotides
			'DA', 'DG', 'DC', 'DT',
			#
			# hydrogen bonding capable nucleotides
			'hDA', 'hDG', 'hDC', 'hDT'
			###
			# Note that these types have different parameters and new bead types
			#  have been created (H0, H1, ...), for example:
			#
			# DA
			# Martini          HADDOCK
			# TA2              aS0
			#
			# hDA
			# Martini          HADDOCK
			# TA2 (TN0 > TP2)  haH0
			#
			# Please refer to the paper 10.1021/acs.jctc.5b00286, figure 1
			# 
			##
			# <WIP> WRITE HERE HOW THESE PARAMETERS WERE OBTAINED <WIP>
			## 
			] 

for nuc in base_list:

	#
	# hydrogen bonding capable nucleotides are mapped to the sabe MARTINI bead types
	#  as the non bondable nucleotides, the following code will identify this nucleotide
	#  according to its bonding capability *bead_type_key* and use this key to find the
	#  correct HADDOCK bead type (the one we created).
	#
	if 'h' in nuc:
		nuc_identifier = nuc[1:]
		bead_type_key = nuc[0]+nuc[-1].lower()
	else:
		nuc_identifier = nuc
		bead_type_key = nuc[-1].lower()

	# Create a dictionary with corresponding indexes for the MARTINI beads
	#  DC -> {0: 'Q0', 1: 'SN0', 2: 'SC2', 3: 'TN0', 4: 'TY2', 5: 'TY3'}
	beads = dict([(i, b) for i, b in enumerate(dna_bb['atom'] + bases[nuc_identifier][0])])

	# There are a few angles that correspond to a bead outside the previously estabilished index range
	#
	# <09032018 Waiting for confirmation from the MARTINI team about this>
	#
	# Use this workaround for now
	# beads[max(beads.keys())+1] = dna_bb['atom'][0] + '*'

	#
	# Start definining the topology
	#

	# Atoms
	atoms = []
	for i in beads:
		m_bead = beads[i]
		atom = atom_name_dic[i]

		h_bead = [e for e in bead_dic if bead_dic[e] == m_bead and bead_type_key in e[:len(bead_type_key)]][0]

		#
		atoms.append('    ATOM %s  type=%s    charge=0.000 end' % (atom, h_bead))


	# DNA BB bonds
	bb_bonds = []
	bb_bonds_params = []
	for i, p in enumerate(dna_con['bond']):
		#
		atomA = atom_name_dic[p[0]]
		atomB = atom_name_dic[p[1]]

		bb_bonds.append('  BOND %s %s' %  (atomA, atomB))


	# DNA BB angles
	bb_angles = []
	# angles_param = []
	for i, p in enumerate(dna_con['angle']):
		#
		atomA = atom_name_dic[p[0]]
		atomB = atom_name_dic[p[1]]
		atomC = atom_name_dic[p[2]]
		#
		bb_angles.append('  ANGLE %s %s %s' % (atomA, atomB, atomC))
		#

	# DNA BB dihedrals
	bb_dih_angles = []
	# dih_param = []
	for i, p in enumerate(dna_con['dih']):
		#
		atomA = atom_name_dic[p[0]]
		atomB = atom_name_dic[p[1]]
		atomC = atom_name_dic[p[2]]
		atomD = atom_name_dic[p[3]]
		#
		bb_dih_angles.append('  DIHEdral %s %s %s %s' % (atomA, atomB, atomC, atomD))

	#================================================================================================================#

	# BASE bonds
	bonds = bb_bonds
	for i, p in enumerate(base_connectivity[nuc_identifier][0]):
		#
		atomA = atom_name_dic[p[0]]
		atomB = atom_name_dic[p[1]]
		#
		bonds.append('  BOND %s %s' % (atomA, atomB))


	# BASE angles
	angles = bb_angles
	for i, p in enumerate(base_connectivity[nuc_identifier][1]):
		#
		atomA = atom_name_dic[p[0]]
		atomB = atom_name_dic[p[1]]
		atomC = atom_name_dic[p[2]]
		#
		m_beadA = beads[p[0]]
		m_beadB = beads[p[1]]
		try:
			m_beadC = beads[p[2]]
		except KeyError:
			# look at table 1 of the paper!
			nP = p[2]-len(beads)
			m_beadC = beads[nP]
			atomC = atom_name_dic[nP]
			#
			# print m_beadA, m_beadB, m_beadC, atomA, atomB, atomC, base_connectivity[nuc_identifier][1][i], p[2], nP, beads[0], atomC
			# print atomA, atomB, 'XX', m_beadA, m_beadB, 'XX', base_connectivity[nuc_identifier][1][i], nuc_identifier
			# exit()
			# angles.append('  ANGLE %s %s MISSING_VALUE' % (atomA, atomB))
			# continue
		# 
		angles.append('  ANGLE %s %s %s' % (atomA, atomB, atomC))
		
	# BASE dihedrals
	dih_angles = bb_dih_angles
	for p in base_connectivity[nuc_identifier][2]:
		
		m_beadA = beads[p[0]]
		m_beadB = beads[p[1]]
		m_beadC = beads[p[2]]
		m_beadD = beads[p[3]]
		
		atomA = atom_name_dic[p[0]]
		atomB = atom_name_dic[p[1]]
		atomC = atom_name_dic[p[2]]
		atomD = atom_name_dic[p[3]]
		
	# Format the topology
	tbw = '''RESIdue %s
  GROUp
%s

%s

%s

%s

END\n\n''' % (nuc, '\n'.join(atoms), '\n'.join(bonds), '\n'.join(dih_angles), '\n'.join(angles))
	#
	print tbw

# done! (:
