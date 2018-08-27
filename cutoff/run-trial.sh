#
RUNN=$1
HADDOCKCMD="/usr/bin/python /home/abonvin/haddock_git/haddock2.4/Haddock/RunHaddock.py"
BENCHMARK_PATH="/home/rodrigo/cutoff-trials"

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

	# Run
	cd run$RUNN
	#echo "## Executing"
	$HADDOCKCMD >& haddock.out
	cd ..

	cd $BENCHMARK_PATH
	
done
