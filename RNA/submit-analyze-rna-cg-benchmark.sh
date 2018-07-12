#
RUNN=$1
SUFFIX=_complex.pdb
HADDOCKCMD="python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py"
BENCHMARK_PATH="/home/rodrigo/rna-benchmark"

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

	if [ ! -d run$RUNN ]; then
		# echo "## Setting up"
		python /home/rodrigo/Nostromo/scripts/prepare_input.py $RUNN --rna
		bash run$RUNN.sh
	fi

	# Run
	cd run$RUNN
	#echo "## Executing"
	$HADDOCKCMD >&/home/rodrigo/rna-benchmark/haddock.out
	cd ..

	# Analyze
	REFERENCE=${TARGET%/}$SUFFIX
	if [ ! -f run$RUNN/water.dat ]; then
		echo "## Running CG analysis"
		python ~/Nostromo/analysis/analyze-run.py $REFERENCE run$RUNN
	fi

	cd $BENCHMARK_PATH
	
done
