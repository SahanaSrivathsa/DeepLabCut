#!/bin/bash
#SBATCH --job-name=DLC_RunBatch   # Job name
#SBATCH --account=barnesca
#SBATCH --time=04:00:00                # Time limit
#SBATCH --nodes=1                      # One node per job
#SBATCH --ntasks=1                     # One task per job
#SBATCH --cpus-per-task= 3              # CPU x mem per CPU 
#SBATCH --mem-per-cpu=6gb               # Memory per cpu 
#SBATCH --array=1-16                    # Array for 8 jobs (1 job per tetrode)
#SBATCH --partition=standard           # Partition (adjust according to your cluster)
#SBATCH --gres=gpu:1                     # Let us say 1 on ocelote that is 16 gb
#SBATCH --array=1


# Load the MATLAB module (adjust the version accordingly)
module load anaconda/2024.06

#Activate Conda
source ~/.bashrc
conda activate deeplabcut

# Navigate to the directory where your MATLAB scripts are located
cd /groups/barnesca/Deeplabcut/BatchScripts

# Run the MATLAB script for the corresponding tetrode in the job array
python /groups/barnesca/Deeplabcut/BatchScripts/wmaze_dlc_batchrun.py