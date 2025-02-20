import deeplabcut
import os
from deeplabcut.utils.auxfun_videos import VideoWriter

video_path=r'G:\WMAZE_Data\Data_Ephys\10894\Session21\PositionData\NewSplitPosTest\2023-09-22_Session21_VT1.mp4'
_, ext = os.path.splitext(video_path)
vid = VideoWriter(video_path)
clips = vid.split(n_splits=10)
#deeplabcut.analyze_videos(config_path, clips, ext)