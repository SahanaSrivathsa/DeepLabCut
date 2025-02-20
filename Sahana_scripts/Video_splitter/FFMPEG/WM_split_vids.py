import os
import importlib.util
import subprocess
import math

# CONFIG
ffmpeg_path = r"C:\Users\sahanasrivathsa\Documents\SYNC\Work\BarnesLab\CODE\Github\DeepLabCut\Sahana_scripts\Video_splitter\ffmpeg-split.py"
base_dir    = r"G:\WMAZE_Data\Data_Ephys\10894\Session21\PositionData\NewSplitPosTest"
n_splits    = 10

# Dynamically load from ffmpeg-split.py
spec = importlib.util.spec_from_file_location("ffmpeg_split", ffmpeg_path)
ffmpeg_split = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ffmpeg_split)

#  Extract reference to the split function
split_video_n_parts = ffmpeg_split.split_video_n_parts

# If you want to track fails:
failed_videos = []

# Iterate over subdirs and process .mp4
for rat_dir in os.listdir(base_dir):
    rat_path = os.path.join(base_dir, rat_dir)
    if not os.path.isdir(rat_path):
        continue  # skip if not directory

    print(f"Processing rat folder: {rat_dir}")
    output_dir = os.path.join(rat_path, "split_output")

    for f in os.listdir(rat_path):
        if f.lower().endswith(".mp4"):
            # Skip if it looks like it's already a split
            if "_split" in f:
                print(f"Skipping {f} because it is already split.")
                continue

            full_path = os.path.join(rat_path, f)
            print(f"Splitting {full_path} into {n_splits} parts")
            try:
                split_video_n_parts(full_path, output_dir, n_splits)
            except Exception as e:
                print(f"Error splitting {full_path}: {e}")
                failed_videos.append(full_path)

print("Failed videos:", failed_videos)
