#!/usr/bin/env bash

SUFFIX=_complex.pdb
#HADDOCKCMD="python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py"
HADDOCKCMD="/home/enmr/software/miniconda2/bin/python2.7 /home/abonvin/haddock_git/haddock2.4/Haddock/RunHaddock.py"
BENCHMARK_PATH="/home/rodrigo/ProtDNA-CG/benchmark/aa"

cd $BENCHMARK_PATH
DIRL="$(ls -d */)"

for TARGET in $DIRL
	do

	cd $TARGET
	echo "########### >> $TARGET <<"
	if [ ! -f run1/structures/it1/water/file.list ];
	then
	    $HADDOCKCMD >& haddock.out
	    bash ~/Nostromo/DNA/patch-dna-AA.sh
	    cd run1
	    $HADDOCKCMD >& haddock.out
	    cd ..
	fi

	# Analyze
	REFERENCE=${TARGET%/}$SUFFIX
	if [ ! -f water.dat ]; then
		echo "## Running AA analysis"
		python ~/Nostromo/analysis/analyze-run.py $REFERENCE run1 --aa
	fi

	cd $BENCHMARK_PATH

done
