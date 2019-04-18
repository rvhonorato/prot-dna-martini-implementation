#!/usr/bin/env bash
# Patch HADDOCK to run CG

DNACG_FOLDER=/home/rodrigo/cg-params

cd run1

# concatenate parameters
#  CG
cat $DNACG_FOLDER/dna-rna-CG-MARTINI-2-1p.top toppar/protein-CG-Martini-2-2.top > toppar/prot-dna-rna_cg.top
cat $DNACG_FOLDER/dna-rna-CG-MARTINI-2-1p.param toppar/protein-CG-Martini-2-2.param > toppar/prot-dna-rna_cg.param
cat $DNACG_FOLDER/dna-rna-CG-MARTINI-2-1p.link toppar/protein-CG-Martini-2-2.link > toppar/prot-dna-rna_cg.link
cat $DNACG_FOLDER/dna-rna-CG-MARTINI-2-1p-break.top toppar/protein_break.top > toppar/prot-dna-rna_break.top

cp $DNACG_FOLDER/patch-types-cg-hbond-dna-rna.cns protocols/
cp $DNACG_FOLDER/patch-breaks-cg-dna-rna.cns protocols/

#  AA
cat toppar/protein-allhdg5-4.top toppar/dna-rna-allatom-hj-opls-1.3.top > toppar/prot-dna-rna.top
cat toppar/protein-allhdg5-4.param toppar/dna-rna-allatom-hj-opls-1.3.param > toppar/prot-dna-rna.param
cat toppar/protein-allhdg5-4-noter.link toppar/dna-rna-1.3.link > toppar/prot-dna-rna.link

echo "> Patching HADDOCK files"
patch protocols/refine.inp -i $DNACG_FOLDER/refine.patch
patch protocols/generate-cg.inp -i $DNACG_FOLDER/generate-cg_nuc.patch
patch run.cns -i $DNACG_FOLDER/run.cns.patch

# edit run.cns
sed -i "s/{===>} dna_mol1=false;/{===>} dna_mol1=true;/g" run.cns # make sure this is correct

#  parameters
sed -i 's/{===>} w_desolv_0=1.0/{===>} w_desolv_0=0.0/g' run.cns
sed -i 's/{===>} w_desolv_1=1.0/{===>} w_desolv_1=0.0/g' run.cns
sed -i 's/{===>} w_desolv_2=1.0/{===>} w_desolv_2=0.0/g' run.cns

sed -i 's/{===>} epsilon_0=10.0/{===>} epsilon_0=78.0/g' run.cns
sed -i 's/{===>} epsilon_1=1.0/{===>} epsilon_1=78.0/g' run.cns
sed -i 's/{===>} epsilon_1=10.0/{===>} epsilon_1=78.0/g' run.cns

sed -i 's/{===>} dielec_0=rdie/{===>} dielec_0=cdie/g' run.cns
sed -i 's/{===>} dielec_1=rdie/{===>} dielec_1=cdie/g' run.cns

# match original AA parameters used in CAPRI
sed -i 's/{===>} structures_0=1000;/{===>} structures_0=4000;/g' run.cns
sed -i 's/{===>} structures_1=200;/{===>} structures_1=400;/g' run.cns
sed -i 's/{===>} waterrefine=200;/{===>} waterrefine=400;/g' run.cns

sed -i 's/{===>} nfle_1=0;/{===>} nfle_1=1;/g' run.cns
sed -i 's/{===>} start_fle_1="";/{===>} start_fle_1="517";/g' run.cns
sed -i 's/{===>} end_fle_1="";/{===>} end_fle_1="519";/g' run.cns

sed -i 's/{===>} tadinit3_t=1000;/{===>} tadinit3_t=500;/g' run.cns

sed -i 's/{===>} dnap_water_tokeep=0.75;/{===>} dnap_water_tokeep=0.25;/g' run.cns
sed -i 's/{===>} water_tokeep=0.50;/{===>} water_tokeep=0.25;/g' run.cns

sed -i 's/{===>} clust_cutoff=0.60;/{===>} clust_cutoff=0.75;/g' run.cns

#  topologies,params and patches
sed -i "s/{===>} prot_cg_top_mol1=\"protein-CG-Martini-2-2.top\";/{===>} prot_cg_top_mol1=\"prot-dna-rna_cg.top\";/g" run.cns
sed -i "s/{===>} prot_cg_link_mol1=\"protein-CG-Martini-2-2.link\";/{===>} prot_cg_link_mol1=\"prot-dna-rna_cg.link\";/g" run.cns
sed -i "s/{===>} prot_cg_par_mol1=\"protein-CG-Martini-2-2.param\";/{===>} prot_cg_par_mol1=\"prot-dna-rna_cg.param\";/g" run.cns

sed -i "s/{===>} prot_top_mol1=\"protein-allhdg5-4.top\";/{===>} prot_top_mol1=\"prot-dna-rna.top\";/g" run.cns
sed -i "s/{===>} prot_link_mol1=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_mol1=\"prot-dna-rna.link\";/g" run.cns
sed -i "s/{===>} prot_par_mol1=\"protein-allhdg5-4.param\";/{===>} prot_par_mol1=\"prot-dna-rna.param\";/g" run.cns

#sed -i '/patch-bb-cg.cns/a \ inline @RUN:protocols/patch-types-cg-hbond-dna-rna.cns' protocols/generate_mol1-cg.inp
#sed -i '/dna_break.top/a {===>} cgdna_break_infile="RUN:toppar/prot-dna-rna_break.top";' protocols/generate_mol1-cg.inp
#sed -i '/inline @RUN:protocols\/dna_break.cns/a \ \ \ inline @RUN:protocols\/patch-breaks-cg-dna-rna.cns' protocols/generate_mol1-cg.inp
#sed -i '/pcgbreak_cutoff/a {===>} dnacgbreak_cutoff=10.0;' protocols/generate_mol1-cg.inp
#sed -i '/@@&dna_break_infile/a \ \ \ \ \ @@&cgdna_break_infile' protocols/generate_mol1-cg.inp

#sed -i 's/dna-rna-allatom-hj-opls-1.3.top/prot-dna-rna_cg.top/g' protocols/generate_mol1-cg.inp
#sed -i 's/dna-rna-1.3.link/prot-dna-rna_cg.link/g' protocols/generate_mol1-cg.inp
#sed -i 's/dna-rna-allatom-hj-opls-1.3.param/prot-dna-rna_cg.param/g' protocols/generate_mol1¯-cg.inp

cd ..