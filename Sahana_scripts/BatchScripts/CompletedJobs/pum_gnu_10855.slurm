#!/bin/bash
#SBATCH --job-name=interactive_test_puma
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --time=01:00:00
#SBATCH --account=barnesca
#SBATCH --partition=gpu_standard

module load parallel
module load anaconda/2024.06
source ~/.bashrc
conda activate deeplabcut

# Change directory to where the Python script is located
cd /groups/barnesca/Deeplabcut/BatchScripts

# Start GPU monitoring in the background
nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used --format=csv -l 1 > gpu_usage.csv &
GPU_MON_PID=$!

# Run your parallel tasks (example: two parallel tasks)
seq 3 7 | parallel --jobs 4 "python run_dlc_v1_10855.py {}"

# Stop GPU monitoring after tasks are done
kill $GPU_MON_PID