
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
    atoms = [aares[atom] for atom in centroid.split() if atom in aares.child_dict] ## replace current atoms with cg beads
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