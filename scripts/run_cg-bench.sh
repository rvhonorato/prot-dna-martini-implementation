
cd /data/rodrigo/benchmark
DIRL="$(ls -d */)"
c=_complex.pdb

HADDOCKCMD="python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py"

for p in $DIRL
	do

	cd $p
	echo "################################### $p"

	if [ ! -d run1 ]; then
		# setup the cg run
		python /home/rodrigo/Nostromo/scripts/prepare_input.py
		echo "## Setting up CG run"
		bash run.sh
	fi

	### run
	# cd run1
	# echo "## Executing"
	# $HADDOCKCMD >&haddock.out
	# cd ..
	###

	### analyze cg
	target=${p%/}$c
	if [ ! -f run1/it0.dat ]; then
		echo "## Running CG analysis"/
		python /home/rodrigo/Nostromo/scripts/ana-cg.py $target run1
	fi
	###

	### analyze aa
	if [ -d run2 ]; then
		# echo "# AA run found"
		if [ ! -f run2/it0.dat ]; then
			echo "## Running AA analysis"/
			python /home/rodrigo/Nostromo/scripts/ana-cg.py $target run2 --aa
		fi
	fi
	###
	
	cd /data/rodrigo/benchmark
	
done
