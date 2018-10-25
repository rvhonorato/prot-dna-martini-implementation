#!/usr/bin/env bash
HADDOCKCMD="python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py"

DIRL="$(ls -d */)"
for TARGET in $DIRL
	do

	cd $TARGET
	echo $TARGET

	cp /home/rodrigo/nucleosome/capri/cg-runs-input/* .

	python ~/Nostromo/scripts/martinize-restraints.py ambig.tbl
    python ~/Nostromo/scripts/martinize-restraints.py unambig.tbl

#    $HADDOCKCMD
#
#    bash ~/Nostromo/nucleosome/patch-nuc.sh
#
#    myfile=$(mktemp)
#    # run
#    python ~/Nostromo/scripts/compare-runcns.py run.cns.ori run1/run.cns > $myfile
#    # sort keeping header
#    head -1 $myfile > outputfile
#    sed 1d $myfile | sort >> outputfile
#    rm $myfile
#    mv outputfile run.cns.diff
	cd ..

done
