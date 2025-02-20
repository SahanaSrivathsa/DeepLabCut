#!/usr/bin/env python
import os
import re
import subprocess

# Base directory where rat folders are located
BASE_DIR = r"O:\DEEPLABCUT\CHEETAH_VT_MP4"

# List of rat IDs
RAT_IDS = ['10993']

# Regular expression pattern to extract session, VT number, and the rest of the filename
VT_PATTERN = re.compile(r"^(.*_VT)(\d+)(.*)(\.(mp4|csv))$")

def group_by_session_vt(files_list):
    """Groups files by base name and session, ensuring VT files are correctly ordered."""
    sessions = {}

    for fname in files_list:
        match = VT_PATTERN.match(fname)
        if not match:
            continue

        base, vt, rest, ext, _ = match.groups()
        vt = int(vt)  # Convert VT number to integer
        session_key = f"{base}{rest}"  # Use filename without VT number as the key

        if session_key not in sessions:
            sessions[session_key] = []

        sessions[session_key].append((vt, fname))

    # Sort files within each session group by VT number (VT1, VT2, VT3)
    for key in sessions:
        sessions[key].sort()

    return sessions

def join_mp4_files(input_dir, file_list, output_name):
    """Merges MP4 files using ffmpeg concat demuxer."""
    concat_filename = os.path.join(input_dir, "concat_list.txt")
    with open(concat_filename, "w", encoding="utf-8") as f:
        for fn in file_list:
            f.write(f"file '{os.path.join(input_dir, fn)}'\n")

    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", concat_filename, "-c", "copy", output_name]
    subprocess.run(cmd, check=True)  # Ensures FFmpeg runs correctly and doesn't hang
    os.remove(concat_filename)

def join_csv_files(input_dir, file_list, output_name):
    """Concatenates CSV files line by line, skipping headers except for the first file."""
    with open(output_name, "w", encoding="utf-8", newline="") as outfile:
        for i, fn in enumerate(file_list):
            with open(os.path.join(input_dir, fn), "r", encoding="utf-8") as infile:
                lines = infile.readlines()
                if i == 0:
                    outfile.writelines(lines)
                else:
                    if len(lines) > 3:
                        outfile.writelines(lines[1:])

def move_original_files(input_dir, files_to_move, output_dir):
    """Moves the original source files used in merging to a separate directory."""
    os.makedirs(output_dir, exist_ok=True)
    for file in files_to_move:
        src_path = os.path.join(input_dir, file)
        dest_path = os.path.join(output_dir, file)
        if os.path.exists(src_path):  # Ensure file still exists before moving
            os.rename(src_path, dest_path)

def process_rat_folder(rat_id):
    """Processes the Merged directory of a given rat inside Analyzed."""
    input_dir = os.path.join(BASE_DIR, rat_id, "Analyzed", "Merged")

    if not os.path.exists(input_dir):
        print(f"Skipping {rat_id} (No 'Merged' folder found)")
        return

    print(f"Processing rat {rat_id} in {input_dir}")

    # Folder where merged source files will be moved after all merging is done
    moved_files_dir = os.path.join(input_dir, "Files_with_multiple_parts_per_sess")
    os.makedirs(moved_files_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    mp4_files = [f for f in files if f.lower().endswith(".mp4")]
    csv_files = [f for f in files if f.lower().endswith(".csv")]

    # Group files by session and VT number
    mp4_groups = group_by_session_vt(mp4_files)
    csv_groups = group_by_session_vt(csv_files)

    # Keep track of all files that were merged
    files_to_move = []

    # Process MP4 files, merging only those with VT2 or VT3
    for base, files_info in mp4_groups.items():
        if any(vt > 1 for vt, _ in files_info):  # Merge only if VT2 or VT3 exists
            file_list = [x[1] for x in files_info]
            vt1_name = file_list[0]  # Use VT1 filename as base
            merged_name = vt1_name.replace(".mp4", "_merged.mp4")
            output_mp4 = os.path.join(input_dir, merged_name)

            if len(file_list) > 1:
                print(f"Merging MP4 files into {output_mp4}")
                join_mp4_files(input_dir, file_list, output_mp4)
                files_to_move.extend(file_list)  # Store files for later moving

    # Process CSV files, merging only those with VT2 or VT3
    for base, files_info in csv_groups.items():
        if any(vt > 1 for vt, _ in files_info):  # Merge only if VT2 or VT3 exists
            file_list = [x[1] for x in files_info]
            vt1_name = file_list[0]  # Use VT1 filename as base
            merged_name = vt1_name.replace(".csv", "_merged.csv")
            output_csv = os.path.join(input_dir, merged_name)

            if len(file_list) > 1:
                print(f"Merging CSV files into {output_csv}")
                join_csv_files(input_dir, file_list, output_csv)
                files_to_move.extend(file_list)  # Store files for later moving

    # Move original files that were merged after all processing is complete
    if files_to_move:
        print(f"Moving original source files to {moved_files_dir}")
        move_original_files(input_dir, files_to_move, moved_files_dir)
    else:
        print("No files were moved.")

def main():
    """Iterates through all rats and processes their folders."""
    for rat_id in RAT_IDS:
        process_rat_folder(rat_id)
        print(f"Finished processing rat {rat_id}")

if __name__ == "__main__":
    main()
