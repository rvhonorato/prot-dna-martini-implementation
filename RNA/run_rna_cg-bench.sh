
cd /home/rodrigo/rna-benchmark
DIRL="$(ls -d */)"
c=_complex.pdb

HADDOCKCMD="python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py"

for p in $DIRL
	do

	cd $p
	echo "################################### $p"

	if [ ! -d run2 ]; then	
		echo "## Setting up run"
		python /home/rodrigo/Nostromo/scripts/prepare_input_rna.py
		bash run.sh
	fi

	### analyze cg
	if [ ! -f run2/water.dat ]; then
		
		cd run2
		echo "## Executing"
		$HADDOCKCMD >&/home/rodrigo/rna-benchmark/haddock.out
		cd ..

		echo "## Running CG analysis"/
		target=${p%/}$c
	 	python /home/rodrigo/Nostromo/scripts/ana-cg.py $target run2
	fi
	###
	
	cd /home/rodrigo/rna-benchmark
	
done
