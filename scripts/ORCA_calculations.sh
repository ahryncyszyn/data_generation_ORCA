#!/bin/bash

# define the path to the parent directory
parent_path="/hkfs/work/workspace/scratch/mt4181-orca/inputs"

# check if the parent directory exists
if [ ! -d "$parent_path" ]; then
    echo "Specified path does not exist!"
    exit 1
fi

# find each subdirectory and submit the job using sbatch
find "$parent_path" -mindepth 1 -type d | while read -r subdirectory; do

    # Check if the "run" file exists in the subdirectory
    if [ -f "$subdirectory/run" ]; then
        echo "Submitting job for $subdirectory"
        
        # Change to the subdirectory and submit the job
        cd "$subdirectory" || continue

        # Submit the job using sbatch
        sbatch run
    else
        echo "No 'run' file in $subdirectory, skipping..."
    fi

done