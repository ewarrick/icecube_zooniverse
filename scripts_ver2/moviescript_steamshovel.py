#Movie Making Script for Steamshovel
#THIS SCRIPT IS FOR MAKING MOVIES ONLY, SEE FILE FILTERSQ.PY

#importing packages
import os
import argparse
import sys
from icecube import icetray, dataclasses
import numpy as np
from icecube.shovelart import PyQColor
#where prediction of each type of event is stored in P frame:
    # skim_pred = frame['ml_suite_classification'].values()[0]
    # cascade_pred = frame['ml_suite_classification'].values()[1]
    # tgtrack_pred = frame['ml_suite_classification'].values()[2]
    # starttrack_pred = frame['ml_suite_classification'].values()[3]
    # stoptrack_pred = frame['ml_suite_classification'].values()[4]

#######FOLDERS SETUP#######

#Makes folders for videos and stills of currently open i3 file.
fileindex = 0 #start folder naming convention at 0.
print("Making Directories...")

file_path = '/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run21971/'

while os.path.isdir(file_path+'Stills{:04}'.format(fileindex)):
    fileindex+=1

outdir_stills=file_path+'Stills{:04}/'.format(fileindex)
os.mkdir(outdir_stills)

#folder for movies
while os.path.isdir(file_path+'Film{:04}'.format(fileindex)):
    fileindex+=1

outdir=file_path+'Film{:04}/'.format(fileindex)
os.mkdir(outdir)

print('Check if Directories are made.')

#######PREP I3 FILE######

app.files.selectFrame(0) #start by selecting 0th frame every new i3 file.
imageNum = int(app.files.nFrames) - 1 #use for ending index, subtract 1 bc nFrames doesn't start its counting at 0.

print("Total Number of Frames (starting from zero):", imageNum) #starts from 0.

app.files.nextMatchingFrame(icetray.I3Frame.DAQ) #Goes to first Q frame of i3 file.
starting_index = int(app.files.currentIndex) #saves the index of the first q frame in i3 file.

window.gl.backgroundColor = PyQColor(80,80,80,255) #sets background color (in this case to grey) in terms of RGB values.


#####LOOP THROUGH FRAMES IN CURRENTLY OPENED I3 FILE########
#Make sure steamshovel is opened and has correct displays selected and the camera is at a good starting point.

for i in range(starting_index,imageNum):

    #Get basic data of frame.
    event_id = str(frame['I3EventHeader'].event_id)
    run_id = str(frame['I3EventHeader'].run_id)
    frame_index = str(app.files.currentIndex)

    #Change colorbar according to time of event, code from Mike C.
    pm = dataclasses.I3RecoPulseSeriesMap.from_frame(frame, 'InIceDSTPulses') #Get pulse map
    keys = pm.keys() #Get OMKeys
    times = sorted([pulse.time for key in keys for pulse in pm[key]]) #Get pulse times.
    #Set start and end times.
    start_time = np.median(times) - np.std(times)
    end_time = np.median(times) + np.std(times)
    #Changes colorbar for each event.
    window.timeline.minTime = start_time
    window.timeline.maxTime = end_time

    #Begin video-making process.
    print("Now Processing Frame ID: ",event_id,"in run:",run_id, "of Index: ",frame_index, "Out of: ",imageNum)
    #Movie parameters:
    window.movieEngine.height = 480 #height in pixel size
    window.movieEngine.width = 640 #width in pixel size
    window.movieEngine.scaleFactor = 4 #scales up resolution of movie.
    window.movieEngine.rescaleFlag = True #rescales back down to original size, for higher quality.
    window.movieEngine.fps = 10 #frames per second, calculated to rotate detector 90 degrees during movie.
    window.movieEngine.nframes = 170 #total number of frames, calculated to rotate detector 90 degrees during movie.
    window.movieEngine.rotation = 5.3 #in degrees per second, also calcuated to rotate detector/camera 90 degrees.
    window.movieEngine.starttime = 0 #start time in ns.
    window.movieEngine.endtime = 40000 #end time in ns, goes to the end of the event frame.

    #Actually produces movie:
    window.movieEngine.produceStills(outdir_stills) #in order to make the movie, need to also produce stills of each frame.

    window.movieEngine.produceMovie(outdir+'run'+run_id+'_'+'event'+event_id+'_index'+frame_index+'.mp4')

    print("Completed Film Frame ID: ",event_id,"in run:",run_id)
    print("Completed Film Index: ",frame_index, "out of: ", imageNum)

    app.files.nextMatchingFrame(icetray.I3Frame.DAQ) #Go to next Q frame and begin loop over again.

window.close() #Close steamshovel when all frames have been turned into movies. 
