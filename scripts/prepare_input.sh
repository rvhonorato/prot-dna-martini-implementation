#!/bin/bash

COMPLEX=$1

CHAIN1=$2
CHAIN2=$3
CHAIN3=$4

PDB_A=$5
PDB_B=$6
PDB_C=$7


# add chains
echo ""
echo ">> Adding chains and segids:"
echo ">>> A: $PDB_A" 
echo ">>> B: $PDB_B"
echo ">>> C: $PDB_C"

sed -i .bak "s/./A/22" $PDB_A
sed -i .bak "s/./B/22" $PDB_B
sed -i .bak "s/./C/22" $PDB_C

# add segids
sed -i .bak "s/./A/76" $PDB_A
sed -i .bak "s/./B/76" $PDB_B
sed -i .bak "s/./C/76" $PDB_C

# Extract true interface from BOUND complex
echo ""
echo ">> Extracting true interface from $COMPLEX"
python ~/Nostromo/scripts/extract_interface.py $COMPLEX $CHAIN1 $CHAIN2 $CHAIN3

AMBIG=${COMPLEX%.*}.tbl
cp $AMBIG ambig.tbl

# Convert unbound to CG
echo ""
echo ">> Converting to CG"
python ~/Nostromo/aa2cg/aa2cg-prot_dna.py $PDB_A
python ~/Nostromo/aa2cg/aa2cg-prot_dna.py $PDB_B 
python ~/Nostromo/aa2cg/aa2cg-prot_dna.py $PDB_C # this will generate dna_restraints.def


echo ""
echo ">> Retrieving AA2CG mapping"
cat ${PDB_A%.*}_cg_to_aa.tbl ${PDB_B%.*}_cg_to_aa.tbl ${PDB_C%.*}_cg_to_aa.tbl > aa2cg.tbl

PDB_A_CG=${PDB_A%.*}_cg.pdb
PDB_B_CG=${PDB_B%.*}_cg.pdb
PDB_C_CG=${PDB_C%.*}_cg.pdb

echo ""
echo ">> Adding chains and segids to CG structures:"
echo ">>> A: $PDB_A_CG" 
echo ">>> B: $PDB_B_CG"
echo ">>> C: $PDB_C_CG"

sed -i .bak "s/./A/22" $PDB_A_CG
sed -i .bak "s/./B/22" $PDB_B_CG
sed -i .bak "s/./C/22" $PDB_C_CG

sed -i .bak "s/./A/76" $PDB_A_CG
sed -i .bak "s/./B/76" $PDB_B_CG
sed -i .bak "s/./C/76" $PDB_B_CG

echo ""
echo ">> Saving input for HADDOCK"
echo ">>> protA: $PDB_A" 
echo ">>> protB: $PDB_B" 
echo ">>> protC: $PDB_C" 
echo ""
echo ">>> protA_CG: $PDB_A_CG" 
echo ">>> protB_CG: $PDB_B_CG" 
echo ">>> protC_CG: $PDB_C_CG"
echo ""
echo ">>> restraints: ambig.tbl"
echo ">>> CG mapping: aa2cg.tbl"
echo ">>> DNA CG restraints: dna_restraints.def"
echo ">>> DNA AA groups: dna-aa_groups.dat"
echo ""

mkdir input
cp $PDB_A $PDB_B $PDB_C $PDB_A_CG $PDB_B_CG $PDB_C_CG ambig.tbl aa2cg.tbl dna_restraints.def dna-aa_groups.dat input/

echo "~/run-cg-2.sh $PDB_A $PDB_B" > input/prepare-2.sh
echo "~/run-cg-3.sh $PDB_A $PDB_B $PDB_C" > input/prepare-3.sh









