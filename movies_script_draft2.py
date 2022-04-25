#THIS SCRIPT IS FOR MAKING MOVIES ONLY, FILTERING LOCATED ON ICETRAY

#steam shovel script to make movies of events.
#based on "makeAllImagesFast.py" from Valerie Helmer.

#import necessary packages

import os
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

#Number of images to take, uses app.files.nFrames for all starting on current frame
imageNum = app.files.nFrames

#window.gl.setPerspective(True)
#loop to make movies_script_draft2

#filter to get physics frames only.
# def filter(index, frame):
# 	return frame.Stop == I3Frame.Physics

#always make sure the script is starting at the first P frame.
for i in range(0,10): #has to have a step size that takes into account using only P frames.
    print(i)
    #print(window.frame_filter)
    #filter(i, app.files.selectFrames(i))
    app.files.selectFrame(i)#select ith frame currently open, returns bool to indicuate success of operation.
    window.movieEngine.scaleFactor = 4
    window.movieEngine.rescaleFlag = True
    window.movieEngine.height = 480
    window.movieEngine.width = 640
    window.movieEngine.fps = 10
    window.movieEngine.nframes = 170
    window.movieEngine.rotation = 5.3
    window.movieEngine.starttime = 0
    window.movieEngine.endtime = 40000
    window.movieEngine.produceStills('/home/icecube/Desktop/eliz_zooniverse/imagesdepo_script/')
    window.movieEngine.produceMovie('/home/icecube/Desktop/eliz_zooniverse/'+"draft3filmfromscriptframe" + str(i)+'.mp4')
    app.files.nextMatchingFrame(1)
