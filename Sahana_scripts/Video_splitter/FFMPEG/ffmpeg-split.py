import os
import subprocess
import math
import datetime

def get_video_duration(filename):
    """
    Returns the total video duration (in seconds, float) using ffprobe.
    """
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        filename
    ]
    output = subprocess.check_output(cmd).decode("utf-8").strip()
    return float(output)

def hhmmss_format(seconds):
    """
    Given a float number of seconds, return 'HH:MM:SS.sss' string.
    Using datetime for robust time formatting up to microseconds.
    """
    # Convert to microseconds
    microseconds = int(round(seconds * 1e6))
    td = datetime.timedelta(microseconds=microseconds)
    # datetime.timedelta can produce days, hours, minutes, seconds,
    # but typically for short durations, days=0.
    # Manually format H:M:S.f
    # or you can do str(td) but it won't always produce HH:MM:SS
    # if < 1 day. So let's do custom:
    total_seconds = td.total_seconds()
    hours = int(total_seconds // 3600)
    mins = int((total_seconds % 3600) // 60)
    secs = (total_seconds % 60)
    return f"{hours:02}:{mins:02}:{secs:06.3f}"

def split_video_no_loss(filename, output_dir, n_splits, tolerance=0.01):
    """
    Splits `filename` into n parts, attempting no duration loss,
    and logs durations of each chunk. If mismatch occurs, logs which chunk.

    Parameters
    ----------
    filename : str
        Path to the original video.
    output_dir : str
        Folder where split files go.
    n_splits : int
        Number of parts to split into.
    tolerance : float
        Allowed mismatch in seconds for each chunk or total.

    Returns
    -------
    A list of output paths for the chunks.
    """
    if not os.path.exists(filename):
        print(f"File does not exist: {filename}")
        return []

    #Get total duration
    orig_duration = get_video_duration(filename)
    if orig_duration <= 0:
        print(f"Unable to get valid duration for {filename}")
        return []

    # Make sure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filebase = os.path.splitext(os.path.basename(filename))[0]
    fileext = os.path.splitext(filename)[1]

    # chunk boundaries [start_0, start_1, ..., start_n], where start_0 = 0, start_n=orig_duration
    # This avoids floating drift by re-accumulating.
    chunk_length = orig_duration / n_splits

    # store a list of (start_time, end_time) in seconds
    chunk_boundaries = []
    accumulated = 0.0
    for i in range(n_splits):
        start = accumulated
        # If not last chunk, normal chunk_length; else go to end
        if i < (n_splits - 1):
            end = start + chunk_length
        else:
            end = orig_duration
        chunk_boundaries.append((start, end))
        accumulated = end  # for next iteration

    #Actually run FFmpeg with -ss and -to for each chunk
    # Using -ss / -to (rather than -t) can yield more precise splits
    splitted_files = []
    base_cmd = ["ffmpeg", "-y",  # or "-n" if you want no overwrite
                "-i", filename,
                "-c", "copy"]

    for idx, (chunk_start, chunk_end) in enumerate(chunk_boundaries, start=1):
        output_path = os.path.join(output_dir, f"{filebase}_split{idx}{fileext}")
        # Format times as HH:MM:SS.sss
        start_str = hhmmss_format(chunk_start)
        end_str   = hhmmss_format(chunk_end)
        # Use -ss <start> -to <end> to cut from start to end
        ffmpeg_cmd = base_cmd + [
            "-ss", start_str,
            "-to", end_str,
            output_path
        ]
        print("About to run:", " ".join(ffmpeg_cmd))
        subprocess.check_call(ffmpeg_cmd)
        splitted_files.append(output_path)

    # 4) Now measure durations of each chunk, check mismatch
    # Save results to a log in the same folder as original
    sum_of_chunks = 0.0
    log_folder = os.path.dirname(filename)
    duration_log = os.path.join(log_folder, f"{filebase}_durations.txt")

    with open(duration_log, "w") as f:
        f.write(f"Original video: {filename}\n")
        f.write(f"Original total duration: {orig_duration:.3f} seconds\n\n")
        f.write("Chunk results:\n")

        for idx, (chunk_start, chunk_end) in enumerate(chunk_boundaries, start=1):
            part_dur_expected = chunk_end - chunk_start
            part_file = splitted_files[idx - 1]
            part_dur_actual = get_video_duration(part_file)

            sum_of_chunks += part_dur_actual
            mismatch = abs(part_dur_expected - part_dur_actual)

            line = (
                f"Part {idx} => Start: {chunk_start:.3f}s, End: {chunk_end:.3f}s, "
                f"Expected ~{part_dur_expected:.3f}s, Actual ~{part_dur_actual:.3f}s"
            )
            if mismatch > tolerance:
                line += f"  [** MISMATCH (~{mismatch:.3f}s) **]"
            f.write(line + "\n")

        # Compare total sum vs original
        f.write("\n--------------------------------------------------\n")
        diff_total = abs(orig_duration - sum_of_chunks)
        f.write(f"Sum of chunk durations = {sum_of_chunks:.3f}s\n")
        if diff_total > tolerance:
            f.write(
                f"WARNING: Overall mismatch from original is ~{diff_total:.3f}s!\n"
                "Check which chunk(s) triggered the mismatch.\n"
            )
        else:
            f.write("No significant overall mismatch.\n")

    return splitted_files
