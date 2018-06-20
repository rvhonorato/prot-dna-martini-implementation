# Implementing Martini DNA coarse grained forcefield in HADDOCK

Most of this was based on the previous implementation done by Jorge Roel for CG protein-protein docking and Marc for Protein-DNA

* Parmeters
	dna-rna-CG-MARTINI-2-1p.top
	dna-rna-CG-MARTINI-2-1p.param
	dna-rna-CG-MARTINI-2-1p.link
	dna-rna-CG-MARTINI-2-1p-break.top

* Patches
	patch-breaks-cg-dna-rna.cns
	patch-types-cg-hbond-dna-rna.cns

* Templates
	template-dna-rna-aa-restraints.def
	template-dna-rna-cg-restraints.def

***

Step 1: Parameter and topology conversion
Step 2: Implement DNA in aa2cg script
Step 3: Patch HADDOCK to use new files
Step 4: Benchmarking
Step 5: Case studies

***

## Step 1: Parameter and topology conversion

First step is to convert MARTINI parameter and write a topology file. The parameters were extracted from the martinize.py script provided by the MARTINI group, the martini_v2.1P-dna.itp forcefield file and the DNA/RNA extension papers.

### Bead renaming

Table S1 (DNA) and S2 (RNA) of its respective papers, providesthe MARTINI Nucleotide bead mapping table; bead, bead type and mapped atoms. All nucleotides like TN0 as bead type, CNS cannot handle this type of repetition. Also parameters obtained for RNA bases differ from DNA, so new bead types were created from them as well <figure>.  The MARTINI DNA/RNA forcefield also has eight special beads with different parameters to account for the hydrogen bonding of the bases, these beads were also renamed.

### Topology - dna-rna-CG-MARTINI-2-1.top

1. Masses
	The atomic mass for each residue is extracted from the first section of the forcefield file, ex:
	```
	; name mass charge ptype c6 c12
      TA2    0     45.000      0.000     A   0.0           0.0
  	  TA3    0     45.000      0.000     A   0.0           0.0
    ```
	Beads TA2 and TA3 have been renamed to NH1 and NH2, the CNS topology then becomes:
	```
	MASS NH5 45.00
	MASS NH4 45.00
	```

2. Residue definition
	This sections relates **atom names** with its **bead type** and defines the bonds, angles and dihedrals. All this information was extracted from Table 1 of the paper.

	**PRESidue** are special definitions used later in the HADDOCK machinery to change bead types of the special hydrogen bonding nucleotides and create the connectivity across nucleotides.


### Parametrization - dna-rna-CG-MARTINI-2-1.param

MARTINI parameters are given in kJ and nanometers CNS needs kCal (divide by 4.178) and angstrom (multiply by 10). 


1. Bonds (paper/forcefield)

	This is divided into bonded and non-bonded terms. 
	
	* **bonded terms** (paper): 
	```
	[ MARTINI ]
	[ beads	type	position	force constant ]
	BB1-BB2	1	0.360	20000
	
	! CNS !
	! 0.360*10 = 3.600 ! distance
	! 20000/4.178 = 47.870 ! force
	BOND NB1 NB2  47.870 3.600
	```

	* **non-bonded** (forcefield):

	(P2 and P3 are not the same as Bda and SN0, this is just an example)

	```
	[ MARTINI ]
	[ nonbond_params ]
      P2       P2  1  4.700000e-01 4.500000e+00 ; self
      P2       P3  1  4.700000e-01 4.500000e+00 ; cross

    ! CNS !
    ! self-term
    ! 4.7e-1 * 10 = 4.7000 ! sigma
    ! 4.5 / 4.178 = 1.07 ~ 1.1 ! epsilon
    NONBONded	Bda	4.700	1.1	4.700	1.1
    ! cross-term
    ! A = 4 * sigma^12 * eps ! attractive
	! B = 4 * sigma^6  * eps ! repulsive
    ! syntax bead1 bead1 A B A B
    NBFIx	Bda	SN0	389344366.569	36119.917	389344366.569	36119.917
    ```

2. Angles & Dihedrals (paper)
	
	Here the third collumn is degrees (no need to change) only convert force; divide by 417.8

	* Angles:

	```
	[ MARTINI ]
	[ beads	type	position	force constant ] 
	BB1-BB2-BB3	2	110.0	200

	! CNS
	! 200/417.8 = 47.87
	ANGLE NB1 NB2 NB3	47.87	110
	```

	* Dihedrals

	```
	[ MARTINI ]
	[ beads	type	position	force constant ]
	BB1-BB2-BB3-BB1	2	95.0	25

	! CNS
	! 25/417.8 = 0.059 ~ 0.06
	DIHEdral NB1 NB2 NB3 NB1	0.06	2	95
	```

### Link - dna-rna-CG-MARTINI-2-1p.link

This file will be read later by CNS to connect the bases together.

### Break - dna-rna-CG-MARTINI-2-1p-break.top

This file contains a topology tthat will be used to break links that are too large to exist. The cutoff for this is specified in `run.cns`

***

## Step 2: Implement DNA/RNA conversion in aa2cg script

The implementation was based on the previous aa2cg which was based on the martinize script. MARTINI has different bead types for proteins depending on its secondary structure. The script identifies the secondary structure and assigns a (HADDOCK) code to te b-factor column of the converted structure. This code is later used in CNS to change the bead types. Same approach was used to account for the special hydrogen bonding beads for DNA. The new version of aa2cg script identifies if a given base is in a hydrogen bonding geometry and assigns it a code to be patched by CNS later (patch-types-cg-hbond-dna-rna.cns).

It now also outputs two files; dna_restraints.def and dna-aa_groups.dat which can be used to automatically define DNA base pair restraints.

*** 

## Step 3: Patch HADDOCK to use new files

In order to use these new files in HADDOCK two patches were incorporated to protocols/; dna-cg-break.cns that reads dna-CG-MARTINI-2-1p-break.top and breaks links above the threshold (defined in run.cns) and patch-types-cg-hbond-dna.cns that changes the bead types according to the haddock code present on the b-factor collumn of the converted DNA structure.

The parameters must also be copied to the toppar/ folder and changed in run.cns, protocols/generate_X-cg.inp and protocols/refine.inp. The changes are:

* run.cns:

	- Set run for AA/CG DNA and change the parameter path
	- Add new flag for DNA CG restraints 
	- Define DNA AA-CG restraints as true (optional?)

* generate_X-cg.inp

	- Add patch to change the hydrogen bonding bead types
	- Add patch to break wrong DNA links
	- Add path to the DNA break topology
	- Change the default parameters from AA to CG to prefent 3TER/5TER patching

* refine.inp

	- Add the option to enable DNA CG restraints
	```
	! Remove these lines 1360-1362 and 1784-1786 (identation is different here)
	if ($Data.dnarest eq true ) then
	  @RUN:data/sequence/dna-rna_restraints.def
	end if
	
	! Add these
	if ($DATA.dnacgrest eq true ) then
	  @RUN:data/sequence/dna-cg_restraints.def
	else
	  if ($Data.dnarest eq true ) then
	    @RUN:data/sequence/dna-rna_restraints.def
	  end if
	end if
	```
***

## Step 4: Benchmarking

In order to compare the perfomance and precision of the HADDOCK-MARTINI implementation both AA and CG runs must be compared. On a previous work, Marc benchmarked the AA protein-DNA HADDOCK perfomance and most of this data is available. Henceforth, the same restraints were used and a few runs were setup.

	* run1: CG default values
	* run2: AA default values
	* run3: AA epsilon = 78, 
	* run4: CG epsilon = 78, w_desol = 0.0

Also as 

### Step 4.1: Analysis















