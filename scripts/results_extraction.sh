#!/bin/bash
#SBATCH --partition=cpuonly
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --output=orcaresults%j.out
#SBATCH --error=orcaresults%j.error
#SBATCH --job-name=orcaresults

calculations_path=path
results_path=path

python extract_results.py "$calculations_path" "$results_path"