1) Transfer all .mp4 files to a new directory
2)In Matlab 'C:\Users\sahanasrivathsa\Documents\SYNC\Work\BarnesLab\CODE\Github\Analysis_Ephys\Sahana_AnalysisCode\IO\POS_VT' Run MoveVTfiles_rename on folder for rat
This renames the files to session numbers and renames VT.0001 as VT2, etc
3)Run WM_split_vides.py - here to split videos
4) Count the total files that have been split and change that in the batch file array no. for that rat
5) Upload batch scripts to HPC and run
6)Download analyzed files and run WM_join_vids.py to join all files
7) Run WM_MergeVTfiles.py if you want to merge the VT1, VT2 etc files after - this is optional
8) Run Move_DLC_merged_files to reorganize to session folders - for future analyses saves it in PositionData within each session folder (MATALB code in same folder as above)