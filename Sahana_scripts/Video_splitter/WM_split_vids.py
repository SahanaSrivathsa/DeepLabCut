#!/usr/bin/env python
import os
import importlib.util
import csv

## INPUT PARAMS
#Set base dir - changed code so it looks for each folder within this and then iterates over teh sub folders
#See below for execution
ffmpeg_path=r"C:\Users\sahanasrivathsa\Documents\SYNC\Work\BarnesLab\CODE\Github\DeepLabCut\Sahana_scripts\Video_splitter\ffmpeg-split.py"
base_dir=r"O:\DEEPLABCUT\CHEETAH_VT_MP4\Extra_Sess"
n_splits=10

##Load functions from ffmpeg-split.py
spec = importlib.util.spec_from_file_location("ffmpeg_split", ffmpeg_path)
ffmpeg_split = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ffmpeg_split)

get_video_length = ffmpeg_split.get_video_length
ceildiv = ffmpeg_split.ceildiv

#for failed functions
failed_videos = []
# FUNCTIONSS
def split_video_n_parts(filename, output_dir,n_splits):
    if not os.path.exists(filename):
        print(f"Input file {filename} does not exist. Skipping...")
        failed_videos.append(filename)
        return

    try:
        length = get_video_length(filename)
        # Compute approximate segment length (it isnt uniform but roughly)
        num_chunks = n_splits
        split_length = length // num_chunks
        if split_length <= 0:
            print(f"Video {filename} is too short to split into 10 parts.")
            return


        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # ffmpeg command template
        vcodec = "copy"
        acodec = "copy"
        extra = ""
        split_cmd = ["ffmpeg", "-n", "-i",filename, "-vcodec", vcodec, "-acodec", acodec] + extra.split()

        filebase = os.path.splitext(os.path.basename(filename))[0]
        fileext = os.path.splitext(filename)[1]

        for n in range(num_chunks):
            start = split_length * n
            output_path = os.path.join(output_dir, f"{filebase}_split{n+1}{fileext}")
            split_args = ["-ss", str(start), "-t", str(split_length), output_path]

            print("About to run:", " ".join(split_cmd + split_args))
            ffmpeg_split.subprocess.check_output(split_cmd + split_args)

    except (subprocess.CalledProcessError, Exception) as e:
        print(f"Error processing {filename}: {e}")
        failed_videos.append(filename)

## RUNNING THE CODE
#Iterate over all the subdirectories in the base directory and look for .mp4 files within them
for rat_dir in os.listdir(base_dir):
    rat_path = os.path.join(base_dir, rat_dir)
    if not os.path.isdir(rat_path):  #Skip if it's not a dir
        continue

    print(f"Processing rat folder: {rat_dir}")

    #Output directory for split videos inside each rat folder (subfldr)
    output_dir = os.path.join(rat_path, "split_output")

    #Process all .mp4 files in the rat folder or subfldr
    for f in os.listdir(rat_path):
        if f.lower().endswith(".mp4"):
            #Skip already split files
            if "_split" in f:
                print(f"Skipping {f} because it is already split.")
                continue

            full_path = os.path.join(rat_path, f)
            print(f"Splitting {full_path} into {n_splits} parts")
            split_video_n_parts(full_path, output_dir,n_splits)

#%%

#%%

#%%
