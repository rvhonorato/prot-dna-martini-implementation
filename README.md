# Implementing MARTINI DNA/RNA coarse grained forcefield in HADDOCK for protein-nucleic acid docking

* Parmeters
	- `dna-rna-CG-MARTINI-2-1p.top`
	- `dna-rna-CG-MARTINI-2-1p.param`
	- `dna-rna-CG-MARTINI-2-1p.link`
	- `dna-rna-CG-MARTINI-2-1p-break.top`

* Patches
	- `patch-breaks-cg-dna-rna.cns`
	- `patch-types-cg-hbond-dna-rna.cns`

* Templates
	- `template-dna-rna-aa-restraints.def`
	- `template-dna-rna-cg-restraints.def`

*Most of this was based on the previous implementation done by Jorge Roel for CG protein-protein docking and Marc for Protein-DNA.*

Step 1: Bead renaming and parameter/topology conversion

Step 2: Implement DNA/RNA in aa2cg script

Step 3: Patch HADDOCK to use new files

Step 4: Benchmarking

Step 5: Case studies

## Step 1: Bead renaming and parameter/topology conversion

First step is to convert MARTINI forcefield parameters and write a CNS topology file. The parameters were extracted from the the `martini_v2.1P-dna.itp` file and the DNA/RNA extension papers (10.1021/acs.jctc.5b00286, 10.1016/j.bpj.2017.05.043).

### Bead renaming

Supplementary tables from the papers provide the MARTINI Nucleotide bead mapping table (figure below).

![DNA-RNA bead mapping](https://www.ime.usp.br/~rvargas/cg-figs/bead-mapping-dna-rna.png)

The MARTINI forcefield defition has multiple parameters for the same bead type that is present on different sidechains. Since CNS cannot handle this type of data structure, it is necessary to create unique beads bead for each atom of each sidechain of each base. Also parameters obtained for RNA bases differ from DNA, so new bead types were created from them as well.  The MARTINI DNA/RNA forcefield also has eight special beads with different parameters to account for the hydrogen bonding of the bases, these beads were also renamed.

![DNA-RNA bead renaming](https://www.ime.usp.br/~rvargas/cg-figs/martini-haddock-bead-renaming.png)


### Topology `dna-rna-CG-MARTINI-2-1.top`

1. Masses
	The atomic mass for each residue is extracted from the first section of the forcefield file (martini_v2.1P-dna.itp). According to the conversion table, MARTINI bead TA2 and TA3 are renamed to NH1 and NH2: 
	
	```
	[ MARTINI ] 
	; name mass charge ptype c6 c12
	TA2    0     45.000      0.000     A   0.0           0.0
	TA3    0     45.000      0.000     A   0.0           0.0

	! CNS 
	MASS NH5 45.00
	MASS NH4 45.00
	```

2. Residue definition

	This sections relates **atom names** with its **bead type** and defines the bonds, angles and dihedrals. All this information was extracted from the first column (beads) of table 1 and table S3 from DNA and RNA papers, respectively.

	Example:
	```
	RESIdue DA
	  GROUp
	    ATOM BB1  type=NB1     charge=0.000 end
	    ATOM BB2  type=NB2     charge=0.000 end
	    ATOM BB3  type=NB3     charge=0.000 end
	    ATOM SC1  type=ANS1    charge=0.000 end
	    ATOM SC2  type=ANS1    charge=0.000 end
	    ATOM SC3  type=ANS3    charge=0.000 end
	    ATOM SC4  type=ANS2    charge=0.000 end

	  BOND BB1 BB2
	  BOND BB2 BB3
	  BOND BB3 SC1
	  BOND SC1 SC2
	  BOND SC2 SC3
	  BOND SC2 SC4
	  BOND SC2 SC4
	  BOND SC3 SC4
	  BOND SC4 SC1

	  ANGLE BB2 BB3 SC1
	  ANGLE BB3 SC1 SC2
	  ANGLE BB3 SC1 SC4
	  ANGLE SC1 SC2 SC3
	  ANGLE SC2 SC1 SC4
	  ANGLE SC2 SC3 SC4
	  ANGLE SC3 SC4 SC1

	  DIHEdral BB1 BB2 BB3 SC1
	  DIHEdral BB2 BB3 SC1 SC2
	  DIHEdral BB2 BB3 SC1 SC4
	END```


	To account for the special hydrogen bonding beads beads a **PRESidue** is defined in the toplogy. This definition is used later in the HADDOCK machinery to change bead types of the special hydrogen bonding nucleotides and create the connectivity across nucleotides according to a code inserted in the b-factor column by the conversion script (next section).


### Parameters `dna-rna-CG-MARTINI-2-1.param`

Information about the bonded and non-bonded terms come from table 1 and table S3 from DNA and RNA papers, respectively and also from file `martini_v2.1P-dna.itp`. Note that MARTINI parameters are given in kJ and nanometers CNS needs kCal (divide by ????) and angstrom (multiply by 10). 

1. Bonds

	This is divided into bonded and non-bonded terms. 
	
	* bonded terms (paper tables): 
	```
	[ MARTINI ]
	[ beads	type	position	force constant ]
	BB1-BB2	1	0.360	20000
	
	! CNS !
	! 0.360*10 = 3.600 ! distance
	! 20000/4.178 = 47.870 ! force
	BOND NB1 NB2  47.870 3.600
	```

	* non-bonded (forcefield):

	(P2 and P3 are not the same as Bda and SN0, this is just an example)

	```
	[ MARTINI ]
	[ syntax: bead1 bead2 ? sigma epsilon ]
      	P2       P2  1  4.700000e-01 4.500000e+00 ; self-term
      	P2       P3  1  4.700000e-01 4.500000e+00 ; cross-term

	! CNS !
	! syntax self-term: NONBONded bead1 bead2 A B A B
	! A = 4.7e-1 * 10 = 4.7000 ! sigma
	! B = 4.5 / 4.178 = 1.07 ~ 1.1 ! epsilon
	NONBONded	Bda	4.700	1.1	4.700	1.1
	
	! syntax cross-term: NBFIx bead1 bead2 A B A B
	! A = 4 * sigma^12 * eps ! attractive
	! B = 4 * sigma^6  * eps ! repulsive
	NBFIx	Bda	SN0	389344366.569	36119.917	389344366.569	36119.917
	```

2. Angles & Dihedrals
	
	Here the third collumn is degrees (no need to change) only convert force; divide by 417.8

	* Angles:

	```
	[ MARTINI ]
	[ beads	type	position	force constant ] 
	BB1-BB2-BB3	2	110.0	200

	! CNS
	! force = 200/417.8 = 47.87
	! syntax: ANGLE bead1 bead2 bead3 force degrees
	ANGLE NB1 NB2 NB3	47.87	110
	```

	* Dihedrals

	```
	[ MARTINI ]
	[ beads	type	position	force constant ]
	BB1-BB2-BB3-BB1	2	95.0	25

	! CNS
	! force = 25/417.8 = 0.059 ~ 0.06
	! syntax: DIHEdral bead1 bead2 bead3 bead4 force type degrees
	DIHEdral NB1 NB2 NB3 NB1	0.06	2	95
	```

### Link `dna-rna-CG-MARTINI-2-1p.link`

This file will be read later by CNS to connect the bases together, example:

```
link nuc head - DA tail + DA end
link nuc head - DA tail + DC end
link nuc head - DA tail + DG end
link nuc head - DA tail + DT end
```

### Break `dna-rna-CG-MARTINI-2-1p-break.top`

This file contains a topology patch that will be used to break links, bonds between atoms, that are too large to exist. This is used to break links between opposing bases at terminus. The cutoff for this break is specified in `run.cns`

```
PRESidue DNCG
   ! patch for deletion of nucleic acid linkage that are too long to exist
  DELETE BOND +BB3 -BB1
  DELETE ANGLE -BB2 -BB3 +BB1
  DELETE ANGLE -BB3 +BB1 +BB2
  DELETE DIHEdral -BB1 -BB2 -BB3 +BB1
  DELETE DIHEdral -BB2 -BB3 +BB1 +BB2
  DELETE DIHEdral -BB3 +BB1 +BB2 +BB3
  DELETE ANGLE -SC1 -BB3 +BB1

END {DNCG}
```

## Step 2: Implement DNA/RNA conversion in aa2cg script

The implementation was based on the previous aa2cg which was based on the martinize script. MARTINI has different bead types for proteins depending on its secondary structure. The script identifies the secondary structure and assigns a code to te b-factor column of the converted structure. This code is later used in CNS to change the bead types according to `PRESidue` definitions in the topology file. 

Same approach was used to account for the special hydrogen bonding beads for DNA/RNA. The new version of aa2cg script identifies if a given base is in a hydrogen bonding geometry measuring euclidian distances for the atoms that should be paired together according to a cutoff and assigns it a code that will be used by `patch-types-cg-hbond-dna-rna.cns`.

For benchmarking purposes It also outputs two files; `dna_restraints.def` and `dna-aa_groups.dat` which can be used to  define DNA/RNA CG base pair restraints.

## Step 3: Patch HADDOCK to use new files

In order to use these new files in HADDOCK two patches were incorporated to `protocols/`; `patch-breaks-cg-dna-rna.cns` that reads `dna-CG-MARTINI-2-1p-break.top` and breaks links above the threshold (defined in `run.cns`) and `patch-types-cg-hbond-dna-rna.cns` that changes the bead types according to the code present on the b-factor collumn of the converted DNA/RNA structure.

To enable HADDOCK to use this CG information, the parameters and topologies must be copied to the `toppar/` folder and some edits are needed in `run.cns`, `protocols/generate_X-cg.inp` and `protocols/refine.inp`:

* `run.cns`:

	- Set CG flag for all molecules:
	- Specify DNA/RNA	
	- Change DNA/RNA chain AA top/link/param from default protein to default DNA/RNA
	- Change DNA/RNA chain CG top/link/param path for DNA/RNA molecule 
	- Add option for DNA/RNA CG restraints as true (optional?)
	- Add new evaluate for DNA/RNA CG restraints 
	
	Code:
	```bash 
	$DNA_CHAIN=C
	sed -i 's/{===>} cg_A=false;/{===>} cg_A=true;/g' run.cns
	sed -i 's/{===>} cg_B=false;/{===>} cg_B=true;/g' run.cns
	sed -i 's/{===>} cg_C=false;/{===>} cg_C=true;/g' run.cns
	sed -i "s/{===>} dna_$DNA_CHAIN=false;/{===>} dna_$DNA_CHAIN=true;/g" run.cns
	# set AA parameters
	sed -i "s/{===>} prot_top_$DNA_CHAIN=\"protein-allhdg5-4.top\";/{===>} prot_top_$DNA_CHAIN=\"dna-rna-allatom-hj-opls-1.3.top\";/g" run.cns
	sed -i "s/{===>} prot_link_$DNA_CHAIN=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_$DNA_CHAIN=\"dna-rna-1.3.link\";/g" run.cns
	sed -i "s/{===>} prot_par_$DNA_CHAIN=\"protein-allhdg5-4.param\";/{===>} prot_par_$DNA_CHAIN=\"dna-rna-allatom-hj-opls-1.3.param\";/g" run.cns
	# set CG parameters
	sed -i "s/{===>} prot_cg_top_$DNA_CHAIN=\"protein-CG-Martini-2-2.top\";/{===>} prot_cg_top_$DNA_CHAIN=\"dna-rna-CG-MARTINI-2-1p.top\";/g" run.cns
	sed -i "s/{===>} prot_cg_link_$DNA_CHAIN=\"protein-CG-Martini-2-2.link\";/{===>} prot_cg_link_$DNA_CHAIN=\"dna-rna-CG-MARTINI-2-1p.link\";/g" run.cns
	sed -i "s/{===>} prot_cg_par_$DNA_CHAIN=\"protein-CG-Martini-2-2.param\";/{===>} prot_cg_par_$DNA_CHAIN=\"dna-rna-CG-MARTINI-2-1p.param\";/g" run.cns
	sed -i '/evaluate (&Data.dnarest = &dnarest_on)/a evaluate (&Data.dnacgrest = &dnacgrest_on)' run.cns
	# default for benchmark
   	sed -i '/{===>} dnarest_on=false;/a {===>} dnacgrest_on=true;' run.cns 
	sed -i "s/{===>} dnarest_on=false;/{===>} dnarest_on=true;/g" run.cns
	sed -i 's/{===>} solvshell=true;/{===>} solvshell=false;/g' run.cns```

* `generate_X-cg.inp`

	- Add patch to change the hydrogen bonding bead types
	- Add patch to break wrong DNA links
	- Add path to the DNA break topology
	- Change the default parameters from AA to CG to prefent 3TER/5TER patching
	
	Code:
	```Bash
	sed -i '/patch-bb-cg.cns/a \ inline @RUN:protocols/patch-types-cg-hbond-dna-rna.cns' protocols/generate_$DNA_CHAIN-cg.inp
	sed -i '/inline @RUN:protocols\/dna_break.cns/a \ \ \ inline @RUN:protocols\/patch-breaks-cg-dna-rna.cns' protocols/generate_$DNA_CHAIN-cg.inp
	sed -i '/pcgbreak_cutoff/a {===>} dnacgbreak_cutoff=10.0;' protocols/generate_$DNA_CHAIN-cg.inp
	sed -i '/dna_break.top/a {===>} cgdna_break_infile="RUN:toppar/dna-rna-CG-MARTINI-2-1p-break.top";' protocols/generate_$DNA_CHAIN-cg.inp
	sed -i '/@@&dna_break_infile/a \ \ \ \ \ @@&cgdna_break_infile' protocols/generate_$DNA_CHAIN-cg.inp
	# change the default parameters from AA to CG to prevent 3TER/5TER patching
	sed -i 's/dna-rna-allatom-hj-opls-1.3.top/dna-rna-CG-MARTINI-2-1p.top/g' protocols/generate_$DNA_CHAIN-cg.inp
	sed -i 's/dna-rna-1.3.link/dna-rna-CG-MARTINI-2-1p.link/g' protocols/generate_$DNA_CHAIN-cg.inp
	sed -i 's/dna-rna-allatom-hj-opls-1.3.param/dna-rna-CG-MARTINI-2-1p.param/g' protocols/generate_$DNA_CHAIN-cg.inp
	# keep the input generator from trying to setup dihedral restraints in CG
	sed -i 's/dna-rna_restraints.def/dna-rna-cg_restraints.def/g' protocols/generate_$DNA_CHAIN-cg.inp```

* `refine.inp`

	- Enable DNA/RNA CG restraints
	
	Code:
	```bash
	# Remove these lines (1360-1362)
	#
	##if ($Data.dnarest eq true ) then
	##  @RUN:data/sequence/dna-rna_restraints.def
	##end if
	#

	sed -i '1360,1362d' protocols/refine.inp

	# Add these
	#
	##if ($DATA.dnacgrest eq true ) then
	##  @RUN:data/sequence/template-dna-rna-cg_restraints.def
	##else
	##  if ($Data.dnarest eq true ) then
	##    @RUN:data/sequence/dna-rna_restraints.def
	##  end if
	##end if
	#
	sed -i "1360i if (\$Data.dnacgrest eq true ) then\n\ \ @RUN:data/sequence/dna-rna-cg_restraints.def\nelse\n\ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ end if\nend if" protocols/refine.inp 

	# Same, but for other part of the code
	sed -i '1784,1786d' protocols/refine.inp
	# identation is different
	sed -i "1784i \ \ if (\$Data.dnacgrest eq true ) then\n\ \ \ \ @RUN:data/sequence/dna-rna-cg_restraints.def\n\ \ else\n\ \ \ \ if (\$Data.dnarest eq true ) then\n\ \ \ \ \ \ @RUN:data/sequence/dna-rna_restraints.def\n\ \ \ \ end if\n\ \ end if" protocols/refine.inp ```
	
***

## Step 4: Benchmarking

In order to compare the perfomance and precision of the HADDOCK-MARTINI implementation both AA and CG runs must be compared. On a previous work, Marc benchmarked the AA protein-DNA HADDOCK perfomance and most of this data is available. Henceforth, the same restraints were used and a few runs were setup.

* DNA

| Run number | Type | Parameters |
| --- | --- | --- |
| 1 | CG | default
| 2 | AA | default
| 3 | AA | `epsilon=78.0`, `desolv=0.0`
| 4 | CG | `epsilon=78.0`, `desolv=0.0`

* RNA

| Run number | Restraint | Parameters |
| --- | --- | --- |
| 1 | act-pass| `epsilon=78.0`
| 2 | act-pass-nodesol | `epsilon=78.0`, `desolv=0.0`
| 3 | CM | ???
| 4 | CM-nodesol | ???

## Step 5: Analysis

1. CPU speedup
2. Success rate
3. Hit rate













