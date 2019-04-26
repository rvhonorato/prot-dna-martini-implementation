#!/usr/bin/env bash
# Patch HADDOCK to run CG

DNACG_FOLDER=/home/rodrigo/cg-params

cd run1

# concatenate parameters
#  CG
# topology
cat $DNACG_FOLDER/dna-CG-MARTINI-2-1p.top toppar/protein-CG-Martini-2-2.top > toppar/prot-dna_cg.top
# params
cat $DNACG_FOLDER/dna-CG-MARTINI-2-1p.param toppar/protein-CG-Martini-2-2.param > toppar/prot-dna_cg.param
# links
cat $DNACG_FOLDER/dna-CG-MARTINI-2-1p.link toppar/protein-CG-Martini-2-2.link > toppar/prot-dna_cg.link
# breaks
cat $DNACG_FOLDER/dna-CG-MARTINI-2-1p-break.top toppar/protein_break.top > toppar/prot-dna_break.top

cp $DNACG_FOLDER/patch-types-cg-hbond-dna.cns protocols/
cp $DNACG_FOLDER/patch-breaks-cg-dna.cns protocols/

#  AA
# topology
cat toppar/protein-allhdg5-4.top toppar/dna-rna-allatom-hj-opls-1.3.top > toppar/prot-dna-rna.top
# params
cat toppar/protein-allhdg5-4.param toppar/dna-rna-allatom-hj-opls-1.3.param > toppar/prot-dna-rna.param
# link
cat toppar/protein-allhdg5-4-noter.link toppar/dna-rna-1.3.link > toppar/prot-dna-rna.link

echo "> Patching HADDOCK files"
patch protocols/refine.inp -i $DNACG_FOLDER/refine.patch
patch protocols/generate-cg.inp -i $DNACG_FOLDER/generate-cg_nuc.patch
patch protocols/generate.inp -i $DNACG_FOLDER/generate_nuc.patch
patch run.cns -i $DNACG_FOLDER/run.cns.patch

# edit run.cns

#  parameters
sed -i "s/{===>} dna_mol1=false/{===>} dna_mol1=true/g" run.cns # make sure this is correct
sed -i 's/{===>} noecv=true/{===>} noecv=false/g' run.cns
sed -i 's/{===>} autohis=true/{===>} autohis=false/g' run.cns

sed -i 's/{===>} w_desolv_0=1.0/{===>} w_desolv_0=0.0/g' run.cns
sed -i 's/{===>} w_desolv_1=1.0/{===>} w_desolv_1=0.0/g' run.cns
sed -i 's/{===>} w_desolv_2=1.0/{===>} w_desolv_2=0.0/g' run.cns

sed -i 's/{===>} epsilon_0=10.0/{===>} epsilon_0=78.0/g' run.cns
sed -i 's/{===>} epsilon_1=1.0/{===>} epsilon_1=78.0/g' run.cns
sed -i 's/{===>} epsilon_1=10.0/{===>} epsilon_1=78.0/g' run.cns

sed -i 's/{===>} dielec_0=rdie/{===>} dielec_0=cdie/g' run.cns
sed -i 's/{===>} dielec_1=rdie/{===>} dielec_1=cdie/g' run.cns


#  topologies,params and patches
sed -i "s/{===>} prot_cg_top_mol1=\"protein-CG-Martini-2-2.top\";/{===>} prot_cg_top_mol1=\"prot-dna_cg.top\";/g" run.cns
sed -i "s/{===>} prot_cg_link_mol1=\"protein-CG-Martini-2-2.link\";/{===>} prot_cg_link_mol1=\"prot-dna_cg.link\";/g" run.cns
sed -i "s/{===>} prot_cg_par_mol1=\"protein-CG-Martini-2-2.param\";/{===>} prot_cg_par_mol1=\"prot-dna_cg.param\";/g" run.cns

sed -i "s/{===>} prot_top_mol1=\"protein-allhdg5-4.top\";/{===>} prot_top_mol1=\"prot-dna-rna.top\";/g" run.cns
sed -i "s/{===>} prot_link_mol1=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_mol1=\"prot-dna-rna.link\";/g" run.cns
sed -i "s/{===>} prot_par_mol1=\"protein-allhdg5-4.param\";/{===>} prot_par_mol1=\"prot-dna-rna.param\";/g" run.cns

cd ..