#!/bin/bash

COMPLEX=$1
RECEPTOR_CHAIN=$2
LIGAND_CHAIN=$3
U_PDB_A=$4
U_PDB_B=$5

# add chains
sed -i bak "s/./A/22" $U_PDB_A
sed -i bak "s/./B/22" $U_PDB_B

# add segids
sed -i bak "s/./A/76" $U_PDB_A
sed -i bak "s/./B/76" $U_PDB_B

# Extract true interface from BOUND complex
python ~/Nostromo/scripts/extract_interface.py $COMPLEX $RECEPTOR_CHAIN $LIGAND_CHAIN

AMBIG=${COMPLEX%.*}.tbl
cp $AMBIG ambig.tbl

# Convert unbound to CG
python ~/Nostromo/aa2cg/aa2cg-prot_dna.py $U_PDB_A
python ~/Nostromo/aa2cg/aa2cg-prot_dna.py $U_PDB_B

cat ${UPDBA%.*}_cg_to_aa.tbl ${UPDBB%.*}_cg_to_aa.tbl > aa2cg.tbl

UPDBA_CG=${U_PDB_A%.*}_cg.pdb
UPDBB_CG=${U_PDB_B%.*}_cg.pdb

sed -i .bak "s/./A/22" $U_PDB_A_CG
sed -i .bak "s/./B/22" $U_PDB_B_CG
sed -i .bak "s/./A/76" $U_PDB_A_CG
sed -i .bak "s/./B/76" $U_PDB_B_CG

mkdir input
cp $U_PDB_A $U_PDB_B $U_PDB_A_CG $U_PDB_B_CG ambig.tbl aa2cg.tbl input/