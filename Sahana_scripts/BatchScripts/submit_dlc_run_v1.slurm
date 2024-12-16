#!/bin/bash
#SBATCH --job-name=DLC_Rv1   # Job name
#SBATCH --account=barnesca
#SBATCH --time=02:00:00           # Time limit
#SBATCH --nodes=1                 # One node per job
#SBATCH --ntasks=1                # One task per job
#SBATCH --cpus-per-task=6         # Number of CPUs per task
#SBATCH --mem-per-cpu=5gb          # Memory per CPU
#SBATCH --partition=gpu_standard      # Partition
#SBATCH --gres=gpu:nvidia_a100_80gb_pcie_2g.20gb             # GPU (16GB)
#SBATCH --array=0-11              # Adjust this range after checking how many videos you have

module load anaconda/2024.06
source ~/.bashrc
conda activate deeplabcut

# Change directory to where the Python script is located
cd /groups/barnesca/Deeplabcut/BatchScripts

# Run the Python script with the array index passed in
python run_dlc.py ${SLURM_ARRAY_TASK_ID}
