##SETUP DATA FOR EXPERIMENTS

To run an experiment, you would first like to create some dummy data.

In order to do this, you'd need a docker volume so that you can access this data later.

You can rename your volume but here we'll use the volume name `SharesStorage` so if you want to name your volume something else, just rename the instances of `SharesStorage` below.

1. Create the volume: `docker volume create SharesStorage`
2. Run a bash shell using this volume and creating the directory `/shares` in it: `docker run -ti -v ShareStorage:/shares bash`
3. Create a directory `Persistence` in `/shares` in the bash shell that opens from the previous command.
4. Use `exit` to exit the bash shell.

Now you are ready to create data using the command:
`docker-compose run --rm -v SharesStorage:/shares create-data`

Note that this container runs the file `Programs/Source/c_shingles_setup.sh` where you can find the number of iterations of creating 100 dummy (name, shingles) pairs are executed. Change this number of iterations to create more dummy data.


## RUNNING EXPERIMENTS

Now that you have dummy data you can run a full set of search experiments using the command:

`docker-compose run --rm -v SharesStorage:/shares mp-spdz`

This command runs the file `Programs/Source/c_shingles_search.sh`, which in turn runs `Programs/Source/c_shingles_search.mpc`. The sizes of data for which the searches are run is in the list `expSizes` in the `.sh` file. You can modify them here. To run other/partial experiments for parts of the computation, see the file `Programs/Source/c_shingles_search.mpc` file. 

## CODE
The actual code can be found under the `Compiler` directory. In particular, look for the `cshingles_dataset.py` file and those imported by it.
