# Implementing Martini DNA coarse grained forcefield in HADDOCK

Most of this was based on the previous implementation done by <> and Jorge Roel for protein-protein docking

First step was to "convert" MARTINI parameter and write a topology file. The parameters were extracted from the martinize.py script provided by the MARTINI group, the martini_v2.1P-dna.itp forcefield file and the 10.1021/acs.jctc.5b00286 paper.

## Parametrization

1. Bonds
	This is divided into bonded and non-bonded; bonded terms are extracted from the paper and non-bonded from the forcefield. 

	1.1. bonded
	beads


2. Angles

