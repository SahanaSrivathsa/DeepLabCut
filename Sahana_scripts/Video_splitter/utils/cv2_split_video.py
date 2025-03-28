import cv2
import os

def split_video_cv2_no_loss(input_file, n_splits=2, output_dir=None):
    """
    Splits the video at 'input_file' into n_splits parts using pure OpenCV reading/writing,
    ensuring no frames are lost or duplicated.

    Parameters
    ----------
    input_file : str
        Path to the original video file.
    n_splits : int
        Number of parts to split into.
    output_dir : str or None
        Folder where the split videos will be saved. If None, saves alongside original.

    Returns
    -------
    splitted_paths : list
        List of paths to the split video files (in order).
    """
    if not os.path.isfile(input_file):
        print(f"File not found: {input_file}")
        return []

    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print(f"Could not open {input_file}")
        return []

    # Original video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps          = float(cap.get(cv2.CAP_PROP_FPS))
    width        = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height       = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if total_frames == 0:
        print(f"No frames found in {input_file}")
        cap.release()
        return []

    if output_dir is None:
        output_dir = os.path.dirname(input_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name, ext = os.path.splitext(os.path.basename(input_file))
    frames_per_split = total_frames // n_splits
    remainder        = total_frames % n_splits

    splitted_paths = []
    frames_written_per_chunk = []  # We'll track how many frames each chunk wrote

    print(f"Original video '{input_file}' => {total_frames} frames total.")

    for i in range(n_splits):
        chunk_size = frames_per_split + (1 if i < remainder else 0)
        if chunk_size <= 0:
            # In case n_splits > total_frames, some parts might be empty
            splitted_paths.append(None)
            frames_written_per_chunk.append(0)
            continue

        output_name = os.path.join(output_dir, f"{base_name}_split{i+1}{ext}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For .mp4
        out_writer = cv2.VideoWriter(output_name, fourcc, fps, (width, height))

        count_written = 0
        for _ in range(chunk_size):
            ret, frame = cap.read()
            if not ret or frame is None:
                break
            out_writer.write(frame)
            count_written += 1

        out_writer.release()
        splitted_paths.append(output_name)
        frames_written_per_chunk.append(count_written)

        print(f"  -> Wrote {count_written} frames to '{output_name}'")

    cap.release()

    # Create a small log file summarizing frames
    log_name = f"{base_name}_splits_log.txt"
    log_path = os.path.join(output_dir, log_name)
    with open(log_path, "w") as lf:
        lf.write(f"Original video: {input_file}\n")
        lf.write(f"Original total frames: {total_frames}\n\n")
        sum_splits = 0
        for idx, (out_path, cnt) in enumerate(zip(splitted_paths, frames_written_per_chunk), start=1):
            lf.write(f"Split {idx}: {out_path or '[NONE]'} => {cnt} frames\n")
            sum_splits += cnt
        lf.write(f"\nSum of frames in all splits = {sum_splits}\n")
        if sum_splits == total_frames:
            lf.write("No frame loss detected.\n")
        else:
            lf.write(f"WARNING: mismatch of {total_frames - sum_splits} frames!\n")

    return splitted_paths

def merge_videos_cv2_no_loss(files_to_merge, output_path):
    """
    Merges the given list of video files (in order) into a single video,
    using OpenCV reading/writing. No frames lost or duplicated.
    NOTE: All videos must share the same resolution & FPS, or additional processing is needed.

    Params
    files_to_merge : str list -Paths to the video files, in the exact order to be merged.
    output_path : str- Where to save the merged video.

    """
    valid_files = [f for f in files_to_merge if f and os.path.isfile(f)]
    if not valid_files:
        print("No valid input files to merge!")
        return None

    # Use the first valid file to get FPS, size
    cap0 = cv2.VideoCapture(valid_files[0])
    if not cap0.isOpened():
        print(f"Could not open first file: {valid_files[0]}")
        return None

    fps    = float(cap0.get(cv2.CAP_PROP_FPS))
    width  = int(cap0.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap0.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap0.release()

    # Prepare writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    total_frames_merged = 0
    frames_per_input = []  # We'll store the frame count for each input

    for vid_path in valid_files:
        cap = cv2.VideoCapture(vid_path)
        local_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out_writer.write(frame)
            local_count += 1
            total_frames_merged += 1
        cap.release()
        frames_per_input.append((vid_path, local_count))

    out_writer.release()
    print(f"Merged {len(valid_files)} files into '{output_path}' ({total_frames_merged} frames).")

    # Create a log file summarizing frames
    merged_base, merged_ext = os.path.splitext(os.path.basename(output_path))
    log_name = f"{merged_base}_merge_log.txt"
    log_path = os.path.join(os.path.dirname(output_path), log_name)

    with open(log_path, "w") as lf:
        lf.write("Merged videos:\n")
        for (fname, count) in frames_per_input:
            lf.write(f"  {fname} => {count} frames\n")
        lf.write(f"\nOutput file: {output_path}\n")
        lf.write(f"Total frames merged: {total_frames_merged}\n")

    return output_path
