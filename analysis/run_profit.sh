#
import sys, os
input_s = sys.argv[1]

input_s = '1BY4_200w.pdb'

from Bio.PDB import PDBParser

# run HADDOCKTOOLS/contacts for input
contacts_exe = '/home/software/haddock/haddock2.3/tools/contact'
os.system('%s %s 10.0 > contacts.temp' % (contacts_exe, input_s))


