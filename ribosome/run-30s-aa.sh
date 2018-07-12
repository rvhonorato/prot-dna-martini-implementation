
cd run2

# concatenate parameters

sed -i 's/{===>} w_desolv_0=1.0/{===>} w_desolv_0=0.0/g' run.cns
sed -i 's/{===>} w_desolv_1=1.0/{===>} w_desolv_1=0.0/g' run.cns
sed -i 's/{===>} w_desolv_2=1.0/{===>} w_desolv_2=0.0/g' run.cns

sed -i 's/{===>} epsilon=10.0;/{===>} epsilon=78.0;/g' run.cns

# AA
cat toppar/protein-allhdg5-4.top toppar/dna-rna-allatom-hj-opls-1.3.top > toppar/prot-dna-rna.top
cat toppar/protein-allhdg5-4.param toppar/dna-rna-allatom-hj-opls-1.3.param > toppar/prot-dna-rna.param
cat toppar/protein-allhdg5-4-noter.link toppar/dna-rna-1.3.link > toppar/prot-dna-rna.link

sed -i "s/{===>} dna_A=false;/{===>} dna_A=true;/g" run.cns

sed -i "s/{===>} prot_top_A=\"protein-allhdg5-4.top\";/{===>} prot_top_A=\"prot-dna-rna.top\";/g" run.cns
sed -i "s/{===>} prot_link_A=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_A=\"prot-dna-rna.link\";/g" run.cns
sed -i "s/{===>} prot_par_A=\"protein-allhdg5-4.param\";/{===>} prot_par_A=\"prot-dna-rna.param\";/g" run.cns


cd ..
