#!/usr/bin/env bash

DNACG_FOLDER=/home/rodrigo/cg-params
HADDOCKCMD="/home/enmr/software/miniconda2/bin/python2.7 /home/abonvin/haddock_git/haddock2.4/Haddock/RunHaddock.py"
DIR_L=$(ls -d */)

for d in ${DIR_L}
do

    cd $d
    echo "########### >> $d <<"

    if [ ! -f run1/structures/it1/water/file.list ]; then
        DNA_ID=$(tail -c 1 run1.sh)

        if [[ ! -d run1/ ]]; then
            $HADDOCKCMD >& haddock.out
        fi

        cd run1/

        # Apply patch
        patch run.cns -i $DNACG_FOLDER/run.cns-aa.patch

        # Fix dynamic values
        sed -i "s/{===>} dna_mol$DNA_ID=false;/{===>} dna_mol$DNA_ID=true;/g" run.cns
        sed -i "s/{===>} prot_top_mol$DNA_ID=\"protein-allhdg5-4.top\";/{===>} prot_top_mol$DNA_ID=\"dna-rna-allatom-hj-opls-1.3.top\";/g" run.cns
        sed -i "s/{===>} prot_link_mol$DNA_ID=\"protein-allhdg5-4-noter.link\";/{===>} prot_link_mol$DNA_ID=\"dna-rna-1.3.link\";/g" run.cns
        sed -i "s/{===>} prot_par_mol$DNA_ID=\"protein-allhdg5-4.param\";/{===>} prot_par_mol$DNA_ID=\"dna-rna-allatom-hj-opls-1.3.param\";/g" run.cns

        # run
        $HADDOCKCMD >& haddock.out

        cd ..
    fi

    cd ..

done