#!/usr/bin/env bash
#DNA_ID=$1
DNA_ID=$(cat run.param | gawk 'match($0, /PDB_FILE([1-9])=\.\/DNA_unbound.pdb/, a) {print a[1]}')
cd run1

sed -i "s/{===>} dna_mol$DNA_ID=false;/{===>} dna_mol$DNA_ID=true;/g" run.cns
sed -i 's/{===>} w_desolv_0=1.0/{===>} w_desolv_0=0.0/g' run.cns
sed -i 's/{===>} w_desolv_1=1.0/{===>} w_desolv_1=0.0/g' run.cns
sed -i 's/{===>} w_desolv_2=1.0/{===>} w_desolv_2=0.0/g' run.cns

sed -i 's/{===>} epsilon_0=10.0/{===>} epsilon_0=78.0/g' run.cns
sed -i 's/{===>} epsilon_1=1.0/{===>} epsilon_1=78.0/g' run.cns
sed -i 's/{===>} epsilon_1=10.0/{===>} epsilon_1=78.0/g' run.cns

sed -i 's/{===>} dielec_0=rdie/{===>} dielec_0=cdie/g' run.cns
sed -i 's/{===>} dielec_1=rdie/{===>} dielec_1=cdie/g' run.cns
sed -i "s/{===>} dnarest_on=false/{===>} dnarest_on=true/g" run.cns

cp ../dna-rna_restraints.def_unbound data/sequence/dna-rna_restraints.def

cd ..