#!/bin/bash
#SBATCH --time=0-00:10:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH -o output_filter.txt

module load Python/3.10.4
module load GCC/11.3.0  OpenMPI/4.1.4
module load mpi4py/3.1.4

time mpiexec python3 filter_data.py

my-job-stats -a -n -s

