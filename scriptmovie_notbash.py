#Movie Making Script for Steamshovel
#THIS SCRIPT IS FOR MAKING MOVIES ONLY, FILTERING LOCATED ON ICETRAY

#importing packages
import os
import argparse
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

parser = argparse.ArgumentParser(description='reading in frames from file')
parser.add_argument('--frame',type=float)
args = parser.parse_args()
#i=args.frame
#Makes the movies with desired settings in steamshovel.
#File should be filtered to include only P frames via script in Icetray.
#for i in range(0,129): #arbitrary range to create small sample of movies, can increase or decrease as needed.
for i in range(0,129):
    print(i)
    app.files.selectFrame(i) #select ith frame currently open, returns bool to indicuate success of operation.
    window.movieEngine.height = 480 #height in pixel size
    window.movieEngine.width = 640 #width in pixel size
    window.movieEngine.scaleFactor = 4 #scales up resolution of movie.
    window.movieEngine.rescaleFlag = True #rescales back down to original size.
    window.movieEngine.fps = 10 #frames per second, calculated to rotate detector 90 degrees during movie.
    window.movieEngine.nframes = 170 #total number of frames, calculated to rotate detector 90 degrees during movie.
    window.movieEngine.rotation = 5.3 #in degrees per second, also calcuated to rotate detector/camera 90 degrees.
    window.movieEngine.starttime = 0 #start time in ns
    window.movieEngine.endtime = 40000 #end time in ns, goes to the end of the event frame.
    window.movieEngine.produceStills('/home/icecube/Desktop/eliz_zooniverse/imagesdepo_script/')
    #in order to get the movie function to work, need to also produce images of each frame.
    #I chose a random folder to evacuate the images since we don't techincally need them.
    window.movieEngine.produceMovie(f'/home/icecube/Desktop/eliz_zooniverse/bashscriptmovietestframe{str(i)}.mp4') #q only frame with gcd.
    #The above line produces the actual movie and saves in specified location with specified name.
    app.files.advanceFrame(1) #advances to next frame.
