#!/bin/bash
#SBATCH --partition=cpuonly
#SBATCH --time=3-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --output=orca%j.out
#SBATCH --error=orca%j.error
#SBATCH --job-name=orca

module purge
module load orca/5.0.4

cd $SLURM_SUBMIT_DIR
cp alathr_valval.inp $TMP
cd $TMP

nohup ${ORCA_PATH}/orca molecule.inp > ${SLURM_SUBMIT_DIR}/molecule.out

cp * $SLURM_SUBMIT_DIR

exit 0