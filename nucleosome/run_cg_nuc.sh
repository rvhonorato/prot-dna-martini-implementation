
cd run1

# concatenate parameters

# Add CG topology, parameters, link and patches
cat /home/rodrigo/cg-params/dna-rna-CG-MARTINI-2-1p.top toppar/protein-CG-Martini-2-2.top > toppar/prot-dna-rna_cg.top
cat /home/rodrigo/cg-params/dna-rna-CG-MARTINI-2-1p.param toppar/protein-CG-Martini-2-2.param > toppar/prot-dna-rna_cg.param
cat /home/rodrigo/cg-params/dna-rna-CG-MARTINI-2-1p.link toppar/protein-CG-Martini-2-2.link > toppar/prot-dna-rna_cg.link

cat /home/rodrigo/cg-params/dna-rna-CG-MARTINI-2-1p-break.top toppar/protein_break.top > toppar/prot-dna-rna_break.top

cp /home/rodrigo/cg-params/patch-types-cg-hbond-dna-rna.cns protocols/
cp /home/rodrigo/cg-params/patch-breaks-cg-dna-rna.cns protocols/


sed -i "s/{===>} dna_A=false;/{===>} dna_A=true;/g" run.cns

# CG
sed -i 's/{===>} cg_A=false;/{===>} cg_A=true;/g' run.cns
sed -i 's/{===>} cg_B=false;/{===>} cg_B=true;/g' run.cns
sed -i 's/{===>} cg_C=false;/{===>} cg_C=true;/g' run.cns

sed -i "s/{===>} prot_cg_top_A=\"protein-CG-Martini-2-2.top\";/{===>} prot_cg_top_A=\"prot-dna-rna_cg.top\";/g" run.cns
sed -i "s/{===>} prot_cg_link_A=\"protein-CG-Martini-2-2.link\";/{===>} prot_cg_link_A=\"prot-dna-rna_cg.link\";/g" run.cns
sed -i "s/{===>} prot_cg_par_A=\"protein-CG-Martini-2-2.param\";/{===>} prot_cg_par_A=\"prot-dna-rna_cg.param\";/g" run.cns

# AA
cat toppar/protein-allhdg5-4.top toppar/dna-rna-allatom-hj-opls-1.3.top > toppar/prot-dna-rna.top
cat toppar/protein-allhdg5-4.param toppar/dna-rna-allatom-hj-opls-1.3.param > toppar/prot-dna-rna.param
cat toppar/protein-allhdg5-4-noter.link toppar/dna-rna-1.3.link > toppar/prot-dna-rna.link

sed -i "s/{===>} dna_A=false;/{===>} dna_A=true;/g" run.cns

sed -i "s/{===>} prot_top_A=\"protein-allhdg5-4.top\";/{===>} prot_top_A=\"prot-dna-rna.top\";/g" run.cns
sed -i "s/{===>} prot_link_A=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_A=\"prot-dna-rna.link\";/g" run.cns
sed -i "s/{===>} prot_par_A=\"protein-allhdg5-4.param\";/{===>} prot_par_A=\"prot-dna-rna.param\";/g" run.cns

sed -i '/patch-bb-cg.cns/a \ inline @RUN:protocols/patch-types-cg-hbond-dna-rna.cns' protocols/generate_A-cg.inp
sed -i '/dna_break.top/a {===>} cgdna_break_infile="RUN:toppar/prot-dna-rna_break.top";' protocols/generate_A-cg.inp
sed -i '/inline @RUN:protocols\/dna_break.cns/a \ \ \ inline @RUN:protocols\/patch-breaks-cg-dna-rna.cns' protocols/generate_A-cg.inp
sed -i '/pcgbreak_cutoff/a {===>} dnacgbreak_cutoff=10.0;' protocols/generate_A-cg.inp
sed -i '/@@&dna_break_infile/a \ \ \ \ \ @@&cgdna_break_infile' protocols/generate_A-cg.inp

# change the default parameters from AA to CG to prevent 3TER/5TER patching
sed -i 's/dna-rna-allatom-hj-opls-1.3.top/prot-dna-rna_cg.top/g' protocols/generate_A-cg.inp
sed -i 's/dna-rna-1.3.link/prot-dna-rna_cg.link/g' protocols/generate_A-cg.inp
sed -i 's/dna-rna-allatom-hj-opls-1.3.param/prot-dna-rna_cg.param/g' protocols/generate_A-cg.inp

cd ..
