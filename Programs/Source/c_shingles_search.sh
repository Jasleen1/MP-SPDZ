#!/bin/bash

# Parameters
BLS_PRIME=52435875175126190479447740508185965837690552500527637822603658699938581184513
players=4
threshold=1



mkdir Persistence
SHARE_FILES=$(ls /shares/Persistence)
for f in $SHARE_FILES; do
	cat /shares/Persistence/$f > Persistence/$f
done


expSizes=(32 64 128 256 512 1024 2048 4096)

for size in ${expSizes[*]}; do
	echo "***************************\n"
	echo "Compiling for size = ${size}"
	echo "***************************\n"
	#Compile the programs
	for i in c_shingles_search; do
	    echo $size | ./compile.py -D -v -C -F 256 $i || exit 1 
	done

	### UNCOMMENT TO ACTUALLY RUN THE EXPERIMENT
	# exp_runs=(1) #(1 2 3 4 5 6 7 8 9 10)
	# for exp_run in ${exp_runs[*]}; do 
	# 	# Setup the network authentication
	# 	Scripts/setup-ssl.sh 4

		

		
	# 	progs="./malicious-shamir-party.x"

		
	# 	for prog in $progs; do
	# 	    echo "Combined Offline/Online Experiment $prog"
	# 	    for i in 0 1 2 3; do
	# 		$prog -N 4 -t 1 -p $i -P $BLS_PRIME c_shingles_search  & pids[${i}]=$!
	# 	    done
	# 	    for pid in ${pids[*]}; do
	# 		wait $pid
	# 	    done
	# 	done
	# done
done

