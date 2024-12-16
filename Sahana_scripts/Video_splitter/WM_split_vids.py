#!/usr/bin/env python
import os
import importlib.util
import math

## INPUT PARAMS
# Directory with .mp4 files - assumes this as vid type
input_dir = r"C:\Users\sahanasrivathsa\Documents\SYNC\Work\BarnesLab\CODE\DEEPLABCUT\Videos_ToAnalyze\10842"
output_dir = os.path.join(input_dir, "split_output")

# Mkdir
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

## Load functions from ffmpeg-split.py which should be in the same forlder or path
spec = importlib.util.spec_from_file_location("ffmpeg_split", "ffmpeg-split.py")
ffmpeg_split = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ffmpeg_split)

get_video_length = ffmpeg_split.get_video_length
ceildiv = ffmpeg_split.ceildiv

def split_video_into_10_parts(filename, output_dir):
    length = get_video_length(filename)
    # Compute approximate segment length (it isnt uniform but roughly)
    num_chunks = 10
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
    split_cmd = ["ffmpeg", "-i", filename, "-vcodec", vcodec, "-acodec", acodec] + extra.split()

    filebase = os.path.splitext(os.path.basename(filename))[0]
    fileext = os.path.splitext(filename)[1]

    for n in range(num_chunks):
        start = split_length * n
        output_path = os.path.join(output_dir, f"{filebase}_split{n+1}{fileext}")
        split_args = ["-ss", str(start), "-t", str(split_length), output_path]

        print("About to run:", " ".join(split_cmd + split_args))
        ffmpeg_split.subprocess.check_output(split_cmd + split_args)

# Iterate over all mp4 files in input_dir
for f in os.listdir(input_dir):
    if f.lower().endswith(".mp4"):
        # Check if filename already contains "_split"
        if "_split" in f:
            print(f"Skipping {f} because it already appears to be split.")
            continue

        full_path = os.path.join(input_dir, f)
        print(f"Splitting {full_path} into 10 parts...")
        split_video_into_10_parts(full_path, output_dir)
