#!/bin/bash

# Parameters
BLS_PRIME=52435875175126190479447740508185965837690552500527637822603658699938581184513
players=4
threshold=1

#Compile the programs


# for i in c_shingles_create_data; do
#     ./compile.py -D -v -C -F 256 $i || exit 1 
# done

#mkdir Player-Data

# Set up the player inputs	
echo 14 > Player-Data/Input-P0-0
echo 12 > Player-Data/Input-P1-0
echo 8 > Player-Data/Input-P2-0
echo 0 > Player-Data/Input-P3-0

mkdir Persistence
SHARE_FILES=$(ls /shares/Persistence)
# for f in $SHARE_FILES
# do
# 	cat /shares/Persistence/$f > Persistence/$f
# done


sortingSizes=(2 4)

for size in ${sortingSizes[*]}; do
	for i in c_shingles_search; do
	    echo $size | ./compile.py -D -v -C -F 256 $i || exit 1 
	done

	# Setup the network authentication
	Scripts/setup-ssl.sh 4

	

	
	progs="./malicious-shamir-party.x"

	
	for prog in $progs; do
	    echo "Combined Offline/Online Experiment $prog"
	    for i in 0 1 2 3; do
		$prog -N 4 -t 1 -p $i -P $BLS_PRIME c_shingles_search  & pids[${i}]=$!
	    done
	    for pid in ${pids[*]}; do
		wait $pid
	    done
	done
done

# for i in c_shingles_search; do
#     echo 2048 | ./compile.py -D -v -C -F 256 $i || exit 1 
# done





# # Setup the network authentication
# Scripts/setup-ssl.sh 4

# # Set up the player inputs
# mkdir Player-Data
# echo 14 > Player-Data/Input-P0-0
# echo 12 > Player-Data/Input-P1-0
# echo 8 > Player-Data/Input-P2-0
# echo 0 > Player-Data/Input-P3-0


# ## SPDZ style, n-of-n additive encoding
# # Setup online
# echo "Running Fake Offline Phase"
# Scripts/setup-online.sh $players 256 128
# # Run the Online
# echo "SPDZ-style Online Phase"
# for i in 0 1 2 3; do
#     ./Player-Online.x -N 4 -t 1 -F -p $i -P $BLS_PRIME hbmpc_mimc_test  & pids[${i}]=$!
# done
# for pid in ${pids[*]}; do
#     wait $pid
# done

# mkdir Persistence
# progs="./malicious-shamir-party.x"

# SHARE_FILES=$(ls /shares/Persistence)
# for f in $SHARE_FILES
# do
# 	cat /shares/Persistence/$f > Persistence/$f
# done


#Run online

# for prog in $progs; do
#     echo "Combined Offline/Online Experiment $prog"
#     for i in 0 1 2 3; do
# 	$prog -N 4 -t 1 -p $i -P $BLS_PRIME c_shingles_search  & pids[${i}]=$!
#     done
#     for pid in ${pids[*]}; do
# 	wait $pid
#     done
# done

# for i in {1..24}; do
# 	echo "Run number: $i"
# 	# SHARE_FILES=$(ls /shares/Persistence)
# 	# for f in $SHARE_FILES
# 	# do
# 	# 	cat /shares/Persistence/$f > Persistence/$f
# 	# done
# 	for prog in $progs; do
# 	    echo "Combined Offline/Online Experiment $prog"
# 	    for i in 0 1 2 3; do
# 		$prog -N 4 -t 1 -p $i -P $BLS_PRIME c_shingles_create_data & pids[${i}]=$!
# 	    done
# 	    for pid in ${pids[*]}; do
# 		wait $pid
# 	    done
# 	done
# 	SHARE_FILES=$(ls Persistence)
# 	for f in $SHARE_FILES
# 	do
# 		cat Persistence/$f >> /shares/Persistence/$f
# 	done
# done
