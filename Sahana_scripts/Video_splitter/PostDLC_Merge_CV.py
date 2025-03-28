# PostDLC_Merge_CV.py
import os
import re
import importlib.util


# CONFIG PARAMS
cv2_fpath=r"C:\Users\sahanasrivathsa\Documents\SYNC\Work\BarnesLab\CODE\Github\DeepLabCut\Sahana_scripts\Video_splitter\utils\cv2_split_video.py"
base_fldr= r"O:\DEEPLABCUT\NEW_VidsToAnalyze\10944\Analyzed"

def merge_csv_files_no_loss(files_to_merge, output_path):
    """
    Merges multiple CSV files line-by-line.
    Assumes each file has similar columns. The simplest approach is:
      - Take the header from the first file
      - For subsequent files, skip the header
      - Append all lines
    Writes the concatenated CSV to `output_path`.
    """
    if not files_to_merge:
        print("No CSV files to merge!")
        return None

    valid_files = [f for f in files_to_merge if os.path.isfile(f)]
    if not valid_files:
        return None

    header_taken = False
    with open(output_path, "w", encoding="utf-8") as outF:
        for idx, fpath in enumerate(valid_files):
            with open(fpath, "r", encoding="utf-8") as inF:
                lines = inF.readlines()
                if not lines:
                    continue
                if not header_taken:
                    # Write entire file, including header
                    outF.writelines(lines)
                    header_taken = True
                else:
                    # Skip the first line if it looks like a header
                    # (naive approach)
                    outF.writelines(lines[1:])

    print(f"Merged {len(valid_files)} CSV files into '{output_path}'.")
    return output_path

def merge_10_splits_in_folder(base_folder, cv2_split_video_path):
    """
    Looks for files named like "<**>_split<number><**>.<ext>"
    If ext is .mp4 or .csv, and if we have EXACTLY splits 1..10 for a given group,
    we merge them in ascending order into a single output.
      - For .mp4 => uses merge_videos_cv2_no_loss from cv2_split_video.py
      - For .csv => uses our local merge_csv_files_no_loss
    """

    # Load 'merge_videos_cv2_no_loss' module from cv2_split_video.py
    spec = importlib.util.spec_from_file_location("cv2_mod", cv2_split_video_path)
    cv2_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cv2_mod)
    merge_mp4_func = cv2_mod.merge_videos_cv2_no_loss

    # Regex to parse e.g. "myFile_split3_stuff.mp4" => pre="myFile", idx="3", post="_stuff", ext=".mp4"
    # We'll look for EXACT matches of split1..split10.
    split_pattern = re.compile(r"^(?P<pre>.*)_split(?P<idx>\d+)(?P<post>.*)(?P<ext>\.\w+)$")

    # Output folder for merged files
    merged_folder = os.path.join(base_folder, "MergedData")
    if not os.path.exists(merged_folder):
        os.makedirs(merged_folder)

    # group by (pre, post, ext), storing indices => path
    grouped = {}
    for fname in os.listdir(base_folder):
        match = split_pattern.match(fname)
        if not match:
            continue

        pre   = match.group("pre")
        idx_s = match.group("idx")
        post  = match.group("post")
        ext   = match.group("ext").lower() # e.g. ".mp4" or ".csv"

        if ext not in {".mp4", ".csv"}:
            continue # Skip other extensions
        try:
            idx = int(idx_s)
        except ValueError:
            continue

        full_path = os.path.join(base_folder, fname)
        # Key by (pre, post, ext)
        key = (pre, post, ext)
        if key not in grouped:
            grouped[key] = {}
        grouped[key][idx] = full_path

    #For each group, see if we have EXACT splits 1..10
    needed = set(range(1, 11))  # 1..10
    results = {}

    for key, idx_map in grouped.items():
        found = set(idx_map.keys())
        if found == needed:
            # We have EXACT splits 1..10, so let's merge
            pre, post, ext = key
            sorted_keys = sorted(idx_map.keys())  # [1..10 in order]
            ordered_files = [idx_map[k] for k in sorted_keys]

            # Output name: e.g. "myFile_merged_stuff.mp4" or .csv
            out_name = f"{pre}_merged{post}{ext}"
            out_path = os.path.join(merged_folder, out_name)

            if ext == ".mp4":
                #print(f"Merging 10 .mp4 splits for {key} -> {out_name}")
                merge_mp4_func(ordered_files, out_path)
                results[key] = out_path
            elif ext == ".csv":
                #print(f"Merging 10 .csv splits for {key} -> {out_name}")
                merge_csv_files_no_loss(ordered_files, out_path)
                results[key] = out_path
            else:
                print(f"Skipping group {key}, ext {ext} not supported for merging.")
                results[key] = None
        else:
            print(f"Group {key} has splits {found}, need {needed}. Skipping.")
            results[key] = None

    return results


# Optional main:
if __name__ == "__main__":
    out = merge_10_splits_in_folder(base_fldr, cv2_fpath)
    print("FINISHED MERGING")
