#!/bin/bash

# Parameters
BLS_PRIME=52435875175126190479447740508185965837690552500527637822603658699938581184513
players=4
threshold=1

#Compile the programs


for i in c_shingles_create_data; do
    ./compile.py -D -v -C -F 256 $i || exit 1 
done

# mkdir Player-Data

Set up the player inputs	
echo 14 > Player-Data/Input-P0-0
echo 12 > Player-Data/Input-P1-0
echo 8 > Player-Data/Input-P2-0
echo 0 > Player-Data/Input-P3-0

mkdir Persistence

### UNCOMMENT TO APPEND TO PREVIOUSLY CREATED DATA
# SHARE_FILES=$(ls /shares/Persistence)
# for f in $SHARE_FILES; do
# 	cat /shares/Persistence/$f > Persistence/$f
# done



for i in {1..24}; do
	echo "Run number: $i"

	# Setup the network authentication
	Scripts/setup-ssl.sh 4
	progs="./malicious-shamir-party.x"
	for prog in $progs; do
	    echo "Combined Offline/Online Experiment $prog"
	    for i in 0 1 2 3; do
		$prog -N 4 -t 1 -p $i -P $BLS_PRIME c_shingles_create_data & pids[${i}]=$!
	    done
	    for pid in ${pids[*]}; do
		wait $pid
	    done
	done
	SHARE_FILES=$(ls Persistence)
	for f in $SHARE_FILES; do
		echo "${f}"
		cat Persistence/$f >> /shares/Persistence/$f
	done
done
