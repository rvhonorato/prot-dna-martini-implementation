
cd run1


# concatenate parameters

cat toppar/protein-allhdg5-4.top toppar/dna-rna-allatom-hj-opls-1.3.top > toppar/prot-dna.top
cat toppar/protein-allhdg5-4.param toppar/dna-rna-allatom-hj-opls-1.3.param > toppar/prot-dna.param
cat toppar/protein-allhdg5-4-noter.link toppar/dna-rna-1.3.link > toppar/prot-dna.link


sed -i "s/{===>} dna_A=false;/{===>} dna_A=true;/g" run.cns
sed -i "s/{===>} prot_top_A=\"protein-allhdg5-4.top\";/{===>} prot_top_A=\"prot-dna.top\";/g" run.cns
sed -i "s/{===>} prot_link_A=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_A=\"prot-dna.link\";/g" run.cns
sed -i "s/{===>} prot_par_A=\"protein-allhdg5-4.param\";/{===>} prot_par_A=\"prot-dna.param\";/g" run.cns

# change the default parameters from AA to CG to prevent 3TER/5TER patching
sed -i 's/dna-rna-allatom-hj-opls-1.3.top/prot-dna.top/g' protocols/generate_A-cg.inp
sed -i 's/dna-rna-1.3.link/prot-dna.link/g' protocols/generate_A-cg.inp
sed -i 's/dna-rna-allatom-hj-opls-1.3.param/prot-dna.param/g' protocols/generate_A-cg.inp

cd ..
