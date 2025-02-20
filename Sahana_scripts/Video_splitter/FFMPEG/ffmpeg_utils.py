import math
import subprocess

def get_video_length(filename):
    """Returns the total video length in seconds."""
    output = subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", filename
    ]).strip()
    return int(float(output))

def ceildiv(a, b):
    """Ceiling division."""
    return int(math.ceil(a / float(b)))
