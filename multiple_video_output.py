from moviepy.editor import *
from IPython import display

video_1 = VideoFileClip("X:\Limitless\Videos Part 2\Exercise.mp4")
video_2 = VideoFileClip("X:\Limitless\Videos Part 2\Exercise Guide.wmv")

filepaths = ["X:\Limitless\Videos Part 2\Exercise.mp4", "X:\Limitless\Videos Part 2\Exercise Guide.wmv"]

# for filepath in filepaths:
#    display.display(display.Video(filepath, embed=True))

# Import everything needed to edit video clips

# loading video dsa gfg intro video and getting only first 5 seconds
clip1 = VideoFileClip("X:\Limitless\Videos Part 2\Exercise.mp4").subclip(0, 5)

# rotating clip1 by 90 degree to get the clip2
clip2 = clip1.rotate(90)

# rotating clip1 by 180 degree to get the clip3
clip3 = clip1.rotate(180)

# rotating clip1 by 270 degree to get the clip4
clip4 = clip1.rotate(270)

# list of clips
clips = [[clip1, clip2],
         [clip3, clip4]]

# stacking clips
final = clips_array(clips)

# showing final clip
final.ipython_display(width=480)

