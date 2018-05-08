
cd /data/rodrigo/benchmark
DIRL="$(ls -d */)"
c=_complex.pdb

HADDOCKCMD="python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py"

for p in $DIRL
	do

	cd $p
	echo "################################### $p"

	# python /home/rodrigo/Nostromo/scripts/prepare_input.py

	if [ ! -d run1 ]; then
		# setup the cg run
		echo "## Setting up CG run"
		bash run.sh
	fi

	# run
	# cd run1
	# echo "## Executing"
	# $HADDOCKCMD >&haddock.out
	# cd ..

	# analyze cg
	target=${p%/}$c
	if [ ! -f run1/it0.dat ]; then
		# qsub ana-cg.sh
		echo "## Running CG analysis"
		python /home/rodrigo/Nostromo/scripts/ana-cg.py $target run1
	# else
	# 	echo '## CG analysis already done'
	fi

	# analyze aa
	if [ -d run2 ]; then
		# echo "# AA run found"
		if [ ! -f run2/it0.dat ]; then
			# qsub ana-aa.sh
			echo "## Running AA analysis"/
			python /home/rodrigo/Nostromo/scripts/ana-cg.py $target run2 --aa
		# else
		# 	echo '## AA analysis already done'
		fi
	fi
	
	# echo "# done #"
	# echo "###################################"
	cd /data/rodrigo/benchmark
	# exit

done
