#!/usr/bin/env bash
#
RUNN=$1
SUFFIX=_complex.pdb
#HADDOCKCMD="python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py"
HADDOCKCMD="/home/enmr/software/miniconda2/bin/python2.7 /home/abonvin/haddock_git/haddock2.4/Haddock/RunHaddock.py"
BENCHMARK_PATH="/home/rodrigo/ProtDNA-CG/benchmark"

cd $BENCHMARK_PATH
DIRL="$(ls -d */)"


if [ $# -eq 0 ]
  then
    echo "No run number supplied"
    exit
fi

for TARGET in $DIRL
	do

	cd $TARGET
	echo "########### >> $TARGET - run$RUNN <<"

    if [ ! -f run$RUNN/structures/it1/water/file.list ]; then
        python /home/rodrigo/Nostromo/scripts/prepare_input.py $RUNN --dna
        bash run$RUNN.sh
	    # Run
	    cd run$RUNN
	    $HADDOCKCMD >& haddock.out
	    cd ..
    fi
#	# Analyze
#	REFERENCE=${TARGET%/}$SUFFIX
#	if [ ! -f run$RUNN/water.dat ]; then
#		echo "## Running CG analysis"
#		python ~/Nostromo/analysis/analyze-run.py $REFERENCE run$RUNN
#	fi

	cd $BENCHMARK_PATH
	
done
