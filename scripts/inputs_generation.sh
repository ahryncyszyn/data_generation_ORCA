#!/bin/bash
#SBATCH --partition=cpuonly
#SBATCH --time=3-00:00:00
#SBATCH --nodes=1
#SBATCH --output=orcainputs%j.out
#SBATCH --error=orcainputs%j.error
#SBATCH --job-name=orcainputs

dataset_dir=path
output_dir=path
no_batches=1 

python generate_inputs.py "$dataset_dir" "$output_dir" $no_batches