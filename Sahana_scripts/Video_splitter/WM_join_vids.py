#!/usr/bin/env python
import os
import re
import subprocess


# This script does the follwoing things
#    - Identifies all MP4 and CSV split files.
#    - Extracts the "base name" and the split index from each filename using regex.
#    - Groups files by base name (the part before `_split`).
#    - Sorts files by their split index.
#    - For MP4 files: use ffmpeg - (concat demux )
#    - For CSV files: concatenate them line by line, taking headers only from the first file.


# Directory containing split files
input_dir = r"C:\Users\sahanasrivathsa\Documents\SYNC\Work\BarnesLab\CODE\DEEPLABCUT\Videos_ToAnalyze\10842\Analyzed"  # Change to your directory
os.chdir(input_dir)
#Make directory for merged files
merged_dir = os.path.join(input_dir, "Merged")
if not os.path.exists(merged_dir):
    os.makedirs(merged_dir)
# Regex to get split files
pattern = re.compile(r"^(.*)_split(\d+)(.*)$")

# Collect MP4 and CSV files
files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
mp4_files = [f for f in files if f.lower().endswith(".mp4")]
csv_files = [f for f in files if f.lower().endswith(".csv")]

def group_by_base(files_list):
    groups = {}
    for fname in files_list:
        m = pattern.match(fname)
        if not m:
            continue
        base, idx, rest = m.groups()

        full_base = base + rest
        idx = int(idx)
        if full_base not in groups:
            groups[full_base] = []
        groups[full_base].append((idx, fname))
    # sort grousp
    for k in groups:
        groups[k].sort(key=lambda x: x[0])
    return groups

mp4_groups = group_by_base(mp4_files)
csv_groups = group_by_base(csv_files)

# Function to join MP4 files using ffmpeg concat demuxer
def join_mp4_files(file_list, output_name):
    # file_list: list of file names in correct order
    # output_name: final name (without split) generate a temp concat file
    concat_filename = "concat_list.txt"
    with open(concat_filename, "w", encoding="utf-8") as f:
        for fn in file_list:
            f.write(f"file '{os.path.join(input_dir, fn)}'\n")

    # Run ffmpeg concat
    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_filename, "-c", "copy", output_name]
    subprocess.check_call(cmd)
    os.remove(concat_filename)

# Function to join CSV files by concatenating rows
def join_csv_files(file_list, output_name):
    with open(output_name, "w", encoding="utf-8", newline="") as outfile:
        header_written = False
        for i, fn in enumerate(file_list):
            with open(fn, "r", encoding="utf-8") as infile:
                lines = infile.readlines()
                if i == 0:
                    # Write all lines from first file
                    outfile.writelines(lines)
                    header_written = True
                else:
                    # skip header which is the first 3 lines
                    if len(lines) > 3:
                        outfile.writelines(lines[1:])

# Process MP4 groups
for base, files_info in mp4_groups.items():
    # files_info is [(idx, filename), ...], sorted
    file_list = [x[1] for x in files_info]
    # output name is base without split
    # Ensure the extension is .mp4
    if not base.lower().endswith(".mp4"):
        base += ".mp4"
    output_mp4 = os.path.join(merged_dir, base)
    if len(file_list) > 1:
        print(f"Joining MP4 files into {output_mp4}")
        join_mp4_files(file_list, output_mp4)
    else:
        print(f"Only one MP4 file in group {base}, skipping join.")

# Process CSV groups
for base, files_info in csv_groups.items():
    file_list = [x[1] for x in files_info]
    if not base.lower().endswith(".csv"):
        base += ".csv"
    output_csv = os.path.join(merged_dir, base)
    if len(file_list) > 1:
        print(f"Joining CSV files into {output_csv}")
        join_csv_files(file_list, output_csv)
    else:
        print(f"Only one CSV file in group {base}, skipping join.")
