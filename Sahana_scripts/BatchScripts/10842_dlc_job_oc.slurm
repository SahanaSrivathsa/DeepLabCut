#!/bin/bash
#SBATCH --job-name=10842_oc   # Job name
#SBATCH --account=barnesca
#SBATCH --time=18:00:00           # Time limit
#SBATCH --nodes=1                 # One node per job
#SBATCH --ntasks=1                # One task per job
#SBATCH --output=slurm_output/%A_%a.out
#SBATCH --cpus-per-task=5        # Number of CPUs per task
#SBATCH --partition=gpu_standard      # Partition
#SBATCH --gres=gpu:1             # GPU (16GB)
#SBATCH --array=0-81              # Adjust this range after checking how many videos you have

module load anaconda/2024.06
source ~/.bashrc
conda activate deeplabcut

# Change directory to where the Python script is located
cd /groups/barnesca/Deeplabcut/BatchScripts

# Run the Python script with the array index passed in
python run_dlc_v1_10842.py ${SLURM_ARRAY_TASK_ID}
