#!/bin/bash


# REF=$1
REF=1BY4_complex.pdb

# check if segid/chain needs fixing
chain_check="$(head -n 1 $REF | cut -c 22)"
segid_check="$(head -n 1 $REF | cut -c 73)" # why is this 67 and not 73?

if [[ -z "${chain_check// }" ]]; then
	echo 'ref has no chain'
	#$HADDOCKTOOLS/pdb_segid-to-chain $REF > temp.pdb
	#cp temp.pdb $REF
fi
if [[ -z "${segid_check// }" ]]; then
	echo 'ref has no segid'
	#$HADDOCKTOOLS/pdb_chain-to-segid $REF > temp.pdb
	#cp temp.pdb $REF
fi

# go look for the structures
cd run1/structures/it1/water/
cp file.nam file.nam.bak

# fix segid/chain
while read p; do
	chain_check="$(sed -n 43p $p | cut -c22)" # REMARKS end at line 43, keep this in mind
	segid_check="$(sed -n 43p $p | cut -c73)"
	if [[ -z "${chain_check// }" ]]; then
		$HADDOCKTOOLS/pdb_segid-to-chain $p > temp.pdb
		cp temp.pdb $p
	fi
	if [[ -z "${segid_check// }" ]]; then
		$HADDOCKTOOLS/pdb_chain-to-segid $p > temp.pdb
		cp temp.pdb $p
	fi
done < file.nam

# add reference
echo "../../../../$REF" | cat - file.nam > file.nam.rmsdin
head file.nam.rmsdin

structures=`egrep -v "(^$|^#)" file.nam.rmsdin`
reference=`echo $structures | cut -d" " -f1`
chains=$(egrep "^ATOM" $reference | cut -c 22 | uniq | tr -d "\n")

refe_contacts=${reference%%.pdb}_10A.contacts
$HADDOCKTOOLS/contact $reference 10.0 > $refe_contacts
# chains=$(awk '{print $2"\n"$5}' $refe_contacts | sort -u | tr -d "\n")

firstchain=${chains:0:1}
permutations=`$PYTHON26 -c "from itertools import permutations; print '\n'.join([''.join(i) for i in permutations('$chains') if i[0] == '$firstchain'])"`


declare -a ZONES

for p in $permutations # Iterates over permutations
do  
    if [ $diff -eq 0 ]
    then
        zone=${zone}" ZONE ${chains:0:1}* \n FIT \n"
    else
        zone=${zone}" "$zone_align" \n FIT \n"
    fi
    for (( i=1; i<${#chains}; i+=1 )) # Iterates over chains
    do
        pair="RZONE ${chains:$i:1}"
        pair="${pair}*\n"
        zone="${zone}$pair"
    done
    fi
fi

echo $ZONES

exit 1
# echo "Read ${#chains} chains from contacts file: $chains"


# Parse Structure List
reference=`echo $structures | cut -d" " -f1`
echo "Using $reference as reference"
mobi=`echo $structures | cut -d" " -f1-`

chains=$(egrep "^ATOM" $reference | cut -c 22 | uniq | tr -d "\n")


# end
cd ../../../../
