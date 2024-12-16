#!/bin/bash
#SBATCH --job-name=DLC_Rv1   # Job name
#SBATCH --account=barnesca
#SBATCH --time=24:00:00           # Time limit
#SBATCH --nodes=1                 # One node per job
#SBATCH --ntasks=1                # One task per job
#SBATCH --output=slurm_output/%A_%a.out
#SBATCH --cpus-per-task=12        # Number of CPUs per task
#SBATCH --partition=gpu_standard      # Partition
#SBATCH --gres=gpu:2             # GPU (16GB)
#SBATCH --array=0-104              # Adjust this range after checking how many videos you have

module load anaconda/2024.06
source ~/.bashrc
conda activate deeplabcut

# Change directory to where the Python script is located
cd /groups/barnesca/Deeplabcut/BatchScripts

# Run the Python script with the array index passed in
python run_dlc_v1_10848.py ${SLURM_ARRAY_TASK_ID}
