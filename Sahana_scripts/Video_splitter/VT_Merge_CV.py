import os
import re
import shutil
import importlib.util
# CONFIG PARAMS
cv2_fpath=r"C:\Users\sahanasrivathsa\Documents\SYNC\Work\BarnesLab\CODE\Github\DeepLabCut\Sahana_scripts\Video_splitter\utils\cv2_split_video.py"
base_fldr= r"O:\DEEPLABCUT\NEW_VidsToAnalyze\10855\OriginalVideos"


def merge_vt_files_in_folder(base_folder, cv2_split_video_path):
    """
    Looks in `base_folder` for files matching '<prefix>_VT<number>.mp4',
    and merges them in ascending order of <number>.
    The final file is named '<prefix>_VTmerged.mp4', placed in the same folder.
    The original files are moved to a folder called MultipleVTFiles

    Parameters
    ----------
    base_folder : str
        Path to the folder with .mp4 files.
    cv2_split_video_path : str
        Path to the 'cv2_split_video.py' module that has merge_videos_cv2_no_loss function.

    Return
    -------
    dict
      { prefix: output_path or None }, listing results of merging for each group.
    """

    #  Dynamically load the base module with merge_videos_cv2_no_loss
    spec = importlib.util.spec_from_file_location("cv2_mod", cv2_split_video_path)
    cv2_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cv2_mod)

    # cv2_mod.merge_videos_cv2_no_loss' will merge the files
    merge_func = cv2_mod.merge_videos_cv2_no_loss

    #Make the folder for multiple VT Files
    multiple_vt_dir = os.path.join(base_folder, "MultipleVTFiles")
    if not os.path.exists(multiple_vt_dir):
        os.makedirs(multiple_vt_dir)

    #  Find .mp4 files matching '<prefix>_VT<number>.mp4'
    pattern = re.compile(r'^(?P<prefix>.+)_VT(?P<num>\d+)\.mp4$', re.IGNORECASE)
    groups = {}

    for fname in os.listdir(base_folder):
        if not fname.lower().endswith('.mp4'):
            continue
        match = pattern.match(fname)
        if not match:
            continue

        prefix = match.group('prefix')
        num_str = match.group('num')
        try:
            num_val = int(num_str)
        except ValueError:
            continue

        full_path = os.path.join(base_folder, fname)

        # group by prefix
        if prefix not in groups:
            groups[prefix] = {}
        groups[prefix][num_val] = full_path

    # For each prefix, gather the .mp4s in ascending order of VT number
    results = {}
    for prefix, file_map in groups.items():
        sorted_keys = sorted(file_map.keys())  # e.g. [1,2,...]
        ordered_files = [file_map[k] for k in sorted_keys]

        if len(ordered_files) < 2:
            print(f"Skipping merge for '{prefix}' - only found one file.")
            results[prefix] = None
            continue

        # Merge them into **_VTmerged.mp4'
        merged_name = f"{prefix}_VTmerged.mp4"
        merged_path = os.path.join(base_folder, merged_name)
        print(f"Merging {len(ordered_files)} files for '{prefix}' -> {merged_name}")

        out_path = merge_func(ordered_files, merged_path)
        results[prefix] = out_path

        # Move the original input files to 'MultipleVTFiles'
        if out_path:
            for vid_path in ordered_files:
                if os.path.isfile(vid_path):
                    dest_path = os.path.join(multiple_vt_dir, os.path.basename(vid_path))
                    print(f"Moving {vid_path} to {dest_path}")
                    shutil.move(vid_path, dest_path)

    return results


# Optionally, you can run the function directly if this is your main script:
if __name__ == "__main__":
    # Example usage:

    # Merge any sets of files named like <prefix>_VT<number>.mp4
    output = merge_vt_files_in_folder(base_fldr, cv2_fpath)
    print("Merge results:", output)
