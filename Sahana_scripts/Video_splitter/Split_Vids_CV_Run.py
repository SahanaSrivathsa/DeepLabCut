# Suppose you place 'split_video_cv2_no_loss' in a file called 'cv2_split_utils.py'
import os
import importlib.util


#Folder paths
cv2_fpath=r"C:\Users\sahanasrivathsa\Documents\SYNC\Work\BarnesLab\CODE\Github\DeepLabCut\Sahana_scripts\Video_splitter\utils\cv2_split_video.py"
base_fldr= r"O:\DEEPLABCUT\NEW_VidsToAnalyze\10894\split_output"

#Load the module
spec = importlib.util.spec_from_file_location("cv2_split_mod", cv2_fpath)
cv2_split_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cv2_split_mod)  # load the module

# Get list of video files in the path
video_files = [f for f in os.listdir(base_fldr) if f.lower().endswith(".mp4")]

# Split each video file into 10 parts
for video_file in video_files:
    video_path = os.path.join(base_fldr, video_file)
    split_files = cv2_split_mod.split_video_cv2_no_loss(video_path, 10, base_fldr)
    print("Split files:", split_files)

