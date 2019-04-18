#!/usr/bin/env bash

DNACG_FOLDER=/home/rodrigo/cg-params/
DIR_L=$(ls -d */)

for d in ${DIR_L}
do
    echo $d
    cd $d
    DNA_ID=$(tail -c 1 run1.sh)
    echo $DNA_ID
    cd ..
done