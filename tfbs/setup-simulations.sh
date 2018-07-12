# for each complex, copy haddockparam.web from the template and edit it

COMPLEXES_PATH="/home/rodrigo/tfbs/complexes"
PARAM_TEMPLATE="/home/rodrigo/tfbs/haddockparam.web-template"

cd $COMPLEXES_PATH

DIRL="$(ls -d */)"


for TARGET in $DIRL
	do

	PDB=${TARGET%/}
	# echo $PDB

	# copy template
	cp $PARAM_TEMPLATE $COMPLEXES_PATH/$TARGET/haddockparam.web

	# rename nuc
	cp $COMPLEXES_PATH/$TARGET/$PDB.pdb $COMPLEXES_PATH/$TARGET/$PDB.pdb.ori

	sed -i 's/ DG/GUA/g' $COMPLEXES_PATH/$TARGET/$PDB.pdb
	sed -i 's/ DC/CYT/g' $COMPLEXES_PATH/$TARGET/$PDB.pdb
	sed -i 's/ DT/THY/g' $COMPLEXES_PATH/$TARGET/$PDB.pdb
	sed -i 's/ DA/ADE/g' $COMPLEXES_PATH/$TARGET/$PDB.pdb

	# fix it
	sed -i '/ZN/d' $COMPLEXES_PATH/$TARGET/$PDB.pdb
	sed -i 's/HETATM/ATOM  /g' $COMPLEXES_PATH/$TARGET/$PDB.pdb
	sed -i "s/*/'/g" $COMPLEXES_PATH/$TARGET/$PDB.pdb

	grep "ATOM" $COMPLEXES_PATH/$TARGET/$PDB.pdb > $COMPLEXES_PATH/$TARGET/$PDB.pdb.tmp
	mv $COMPLEXES_PATH/$TARGET/$PDB.pdb.tmp $COMPLEXES_PATH/$TARGET/$PDB.pdb
	
 	# python /home/rodrigo/pdb-tools/pdb_splitchain.py $COMPLEXES_PATH/$TARGET/$PDB.pdb

 	# python /home/rodrigo/pdb-tools/pdb_reatom.py -1 $COMPLEXES_PATH/$TARGET/${PDB}_A.pdb > $COMPLEXES_PATH/$TARGET/${PDB}_A.pdb.tmp
	# python /home/rodrigo/pdb-tools/pdb_reatom.py -1 $COMPLEXES_PATH/$TARGET/${PDB}_B.pdb > $COMPLEXES_PATH/$TARGET/${PDB}_B.pdb.tmp
	
 	# python /home/rodrigo/pdb-tools/pdb_reres.py $COMPLEXES_PATH/$TARGET/${PDB}_A.pdb.tmp -resid 1 > $COMPLEXES_PATH/$TARGET/${PDB}_A.pdb
	# python /home/rodrigo/pdb-tools/pdb_reres.py $COMPLEXES_PATH/$TARGET/${PDB}_B.pdb.tmp -resid 1 > $COMPLEXES_PATH/$TARGET/${PDB}_B.pdb

	# cat $COMPLEXES_PATH/$TARGET/${PDB}_A.pdb $COMPLEXES_PATH/$TARGET/${PDB}_B.pdb > $COMPLEXES_PATH/$TARGET/$PDB.pdb

	# replace pdb
	python /home/rodrigo/Nostromo/tfbs/change-pdb.py $COMPLEXES_PATH/$TARGET/haddockparam.web $COMPLEXES_PATH/$TARGET/$PDB.pdb

	# perl /home/rodrigo/haddock-CSB-tools/paramFL_related/replacePDBfl.pl $COMPLEXES_PATH/$TARGET/haddockparam.web $COMPLEXES_PATH/$TARGET/$PDB.pdb 1
	# perl /home/rodrigo/haddock-CSB-tools/paramFL_related/replacePDBfl.pl $COMPLEXES_PATH/$TARGET/haddockparam.web $COMPLEXES_PATH/$TARGET/$PDB.pdb 2

	# submission ready
done

