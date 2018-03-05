### Results from Don

#### Martini - CNS CONVERSION

Topology and parameter files were converted from GROMACS format to CNS format. In order to obtain unique types and corresponding parameters required for CNS, the MARTINI backbone backbone bead names (Table 3.1) and side chain bead names (Table 3.3) were renamed and extended. Corresponding parameters including bond length (D), bond angles (Θ), bond dihedrals (ψ) and corresponding force constants (K) are given in table 3.2 and 3.3 for the backbone -, backbone-side chain- and side chain side chain beads consequently. Force constant units were adjusted from kJ.mol-1 to kcal.mol-1 and from nm to Å.

### Todo

**.top**

The topology statement consists of information about "residues" that combine to form a particular macromolecule. The data include descriptions of atoms, assignments of covalent bonds (connectivity), bond angles, and other information. The information provided by the topology statement is used by the segment statement and the patch statement to generate the molecular structure.