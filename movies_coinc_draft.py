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

#Get camera into position.
window.gl.resetCamera()
window.gl.setPerspective(True)

#List of image names
names = []

#Sets the beginning index to start take images on
i = 0

#Making movies of frames.
for i, num in enumerate(imageNum):
    app.files.selectFrame(i):
        window.movieEngine.scaleFactor(1)
        window.movieEngine.height(480) #Y dimension of the movie output in pixels.
        window.movieEngine.width(640) #X dimension of the movie output in pixels
        window.movieEngine.fps(10) #Frames per second of the output movie.
        window.movieEngine.nframes(170) #Number of frames to render
        window.moviengine.rotation(5.3) #Movie camera rotation in degrees per
                                        #second. Positive numbers rotate the
                                        #camera counterclockwise, and
                                        #negative numbers clockwise.
        window.movieEngine.starttime(0) #Nanosecond of event time
        window.movieEngine.endtime(40000) #Nanosecond of event time on which to
                                            #end the movie recording

        name = (i + url)

        window.movieEngine.produceMovie(names[i] + url) #creates movie with
    names.append(name)                  #ffmpeg, output files will end with mp4
    i = i + 1
