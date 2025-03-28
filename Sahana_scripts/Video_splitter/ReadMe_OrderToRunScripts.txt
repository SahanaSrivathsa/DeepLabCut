1) Transfer all .mp4 files to a new directory
% NOTE THIS STEP IS ONLY FOR WMAZE
2)In Matlab 'C:\Users\sahanasrivathsa\Documents\SYNC\Work\BarnesLab\CODE\Github\Analysis_Ephys\Sahana_AnalysisCode\IO\POS_VT' Run MoveVTfiles_rename on folder for rat
This renames the files to session numbers and renames VT.0001 as VT2, etc
% FOR ALL
3)Run Split_Vids_CV_Run.py - here to split videos (note this needs to be run in a directory that contains DLC installed)
4) Count the total files that have been split and change that in the batch file array no. for that rat
5) Upload batch scripts to HPC and run
6)Download analyzed files/in the folder which contains the files on the HPC run PostDLC_Merge_CV.py to join all files

8) Run Move_DLC_merged_files to reorganize to session folders - for future analyses saves it in PositionData within each session folder (MATALB code in same folder as above)
