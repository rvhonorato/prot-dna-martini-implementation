
HADDOCKCMD="python /home/software/haddock/haddock2.3/Haddock/RunHaddock.py"
for i in $(seq 1 12)
do
	cd run$i
	$HADDOCKCMD >&haddock.out
	cd ..
done