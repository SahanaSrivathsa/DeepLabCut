import os
import sys
import deeplabcut

# Configuration
project = 'wmaze2-ss-2024-12-02'
prefix = '/groups/barnesca/Deeplabcut/DLC_Projects'
projectpath = os.path.join(prefix, project)
config = os.path.join(projectpath, 'config.yaml')

basepath = '/groups/barnesca/Deeplabcut/VideosToAnalyze/10854'
dest_folder='/groups/barnesca/Deeplabcut/VideosToAnalyze/10854/Analyzed'
vtype = '.mp4'
shuffle = 1
trainingsetindex = 0

# Gather all .mp4 files recursively
vid_files = []
for root, dirs, files in os.walk(basepath):
    for f in files:
        if f.endswith(vtype):
            vid_files.append(os.path.join(root, f))

# Get the array index from command line argument
if len(sys.argv) > 1:
    idx = int(sys.argv[1])
else:
    idx = 0
# Select the video for this array task
video = vid_files[idx]

# Run DLC commands on the selected video
deeplabcut.analyze_videos(config, [video], shuffle=shuffle, videotype=vtype, save_as_csv=True)

deeplabcut.filterpredictions(config, [video], shuffle=shuffle, trainingsetindex=trainingsetindex,
                             filtertype='arima', p_bound=0.01, ARdegree=3, MAdegree=1, alpha=0.01,
                             save_as_csv=True,destfolder=dest_folder)

deeplabcut.plot_trajectories(config, [video], shuffle=shuffle, trainingsetindex=trainingsetindex,
                             filtered=True, showfigures=False,destfolder=dest_folder)

deeplabcut.create_labeled_video(config, [video], shuffle=shuffle, trainingsetindex=trainingsetindex,
                                filtered=True, save_frames=False, draw_skeleton=True, trailpoints=0,
                                pcutoff=0.30,destfolder=dest_folder)
