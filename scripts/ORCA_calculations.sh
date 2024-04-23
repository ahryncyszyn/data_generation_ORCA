#!/bin/bash

path="/home/kit/iti/mt4181/test"

if [ ! -d "$path" ]; then
    echo "Specified path does not exist!"
    exit 1
fi

find "$path" -type d | while read -r directory; do
    
    cd "$directory" || continue

    
    if [ -f "molecule.inp" ]; then
        
        sbatch <<EOF
#!/bin/bash
#SBATCH --partition=single
#SBATCH --time=3-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=180000
#SBATCH --output=orca%j.out
#SBATCH --error=orca%j.error
#SBATCH --job-name=orca

module purge
module load orca/5.0.4

cd $SLURM_SUBMIT_DIR
cp molecule.inp $TMP
cd $TMP

nohup ${ORCA_PATH}/orca molecule.inp > ${SLURM_SUBMIT_DIR}/molecule.out

cp * $SLURM_SUBMIT_DIR

exit 0
EOF   

    fi
done