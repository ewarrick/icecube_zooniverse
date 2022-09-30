#Movie Making Script for Steamshovel
#THIS SCRIPT IS FOR MAKING MOVIES ONLY, SEE FILE FILTERSQ.PY

#importing packages
import os
import argparse
import sys
from icecube import icetray, dataclasses
import numpy as np
#from icecube.shovelart import PyQColor

from icecube.shovelart import ActivePixmapOverlay, Arrow, ArtistHandle, ArtistHandleList, ArtistKeylist, BaseLineObject, ChoiceSetting, ColorMap, ColoredObject, ConstantColorMap, ConstantFloat, ConstantQColor, ConstantTime, ConstantVec3d, Cylinder, DynamicLines, FileSetting, I3TimeColorMap, KeySetting, LinterpFunctionFloat, LinterpFunctionQColor, LinterpFunctionVec3d, OMKeySet, OverlayLine, OverlaySizeHint, OverlaySizeHints, ParticlePath, ParticlePoint, Phantom, PixmapOverlay, PyArtist, PyQColor, PyQFont, PyVariantFloat, PyVariantQColor, PyVariantTime, PyVariantVec3d, RangeSetting, Scenario, SceneGroup, SceneObject, SceneOverlay, SolidObject, Sphere, StaticLines, StepFunctionFloat, StepFunctionQColor, StepFunctionTime, StepFunctionVec3d, Text, TextOverlay, TimePoint, TimeWindow, TimeWindowColor, VariantFloat, VariantQColor, VariantTime, VariantVec3d, VariantVec3dList, Vec3dList, ZPlane, vec3d
from icecube.icetray import OMKey
from icecube.icetray import logging
#where prediction of each type of event is stored in P frame:
    # skim_pred = frame['ml_suite_classification'].values()[0]
    # cascade_pred = frame['ml_suite_classification'].values()[1]
    # tgtrack_pred = frame['ml_suite_classification'].values()[2]
    # starttrack_pred = frame['ml_suite_classification'].values()[3]
    # stoptrack_pred = frame['ml_suite_classification'].values()[4]

#######FOLDERS SETUP#######

i3_name = os.path.basename(app.files.openFiles[1])
direc = os.path.dirname(app.files.openFiles[1])
#Makes folders for videos and stills of currently open i3 file.
fileindex = 0 #start folder naming convention at 0.
print("Making Directories...")

file_path = f"{direc}/"
#f'/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run{run_id}/class_type_{str(classtype)}/{greaterorless}_than/cut_{cut_val}'

while os.path.isdir(file_path+'Stills{:04}'.format(fileindex)):
    fileindex+=1

outdir_stills=file_path+'Stills{:04}/'.format(fileindex)
os.mkdir(outdir_stills)

#folder for movies
while os.path.isdir(file_path+'Film{:04}'.format(fileindex)):
    fileindex+=1

outdir=file_path+'Film{:04}/'.format(fileindex)
os.mkdir(outdir)

while os.path.isdir(file_path+'File{:04}_compressed'.format(fileindex)):
    fileindex+=1

outdir_compressed = file_path+'Film{:04}_compressed'.format(fileindex)
os.mkdir(outdir_compressed)

print('Check if Directories are made.')

###SCENARIOS###
scenario = window.gl.scenario
scenario.clear()
artist = scenario.add( 'CoordinateSystem', [] )
scenario.setIsActive( artist, False )
scenario.changeSetting( artist, 'position', '0m, 0m, 0m' )
scenario.changeSetting( artist, 'x length', '1 km' )
scenario.changeSetting( artist, 'y length', '1 km' )
scenario.changeSetting( artist, 'z length', '1 km' )
scenario.changeSetting( artist, 'line width', 1 )
scenario.changeSetting( artist, 'head angle', 20 )
scenario.changeSetting( artist, 'head length', 30 )
scenario.changeSetting( artist, 'opacity', 1 )
scenario.setIsActive( artist, True )

artist = scenario.add( 'Ice', [] )
scenario.setIsActive( artist, False )
scenario.changeSetting( artist, 'Show ice', True )
scenario.changeSetting( artist, 'Show bedrock', True )
scenario.changeSetting( artist, 'Show dust', False )
scenario.changeSetting( artist, '3D dust', False )
scenario.changeSetting( artist, 'Color ice', PyQColor(25,25,255,255) )
scenario.changeSetting( artist, 'Color bedrock', PyQColor(128,102,102,255) )
scenario.changeSetting( artist, 'Color dust', PyQColor(100,100,100,50) )
scenario.changeSetting( artist, 'Plane width', '2200 m' )
scenario.changeSetting( artist, 'Line width', 1 )
scenario.changeSetting( artist, 'Dust density', 1.5 )
scenario.changeSetting( artist, 'Dust scatter', 0.2 )
scenario.setIsActive( artist, True )

artist = scenario.add( 'Detector', ['I3Geometry', ] )
scenario.setIsActive( artist, False )
scenario.changeSetting( artist, 'DOM labels', False )
scenario.changeSetting( artist, 'DOM radius', 1 )
scenario.changeSetting( artist, 'DOM color', PyQColor(255,255,255,255) )
scenario.changeSetting( artist, 'string color', PyQColor(255,255,255,76) )
scenario.changeSetting( artist, 'string width', 1 )
scenario.changeSetting( artist, 'string cross', False )
scenario.changeSetting( artist, 'outline width', 0 )
scenario.changeSetting( artist, 'high quality DOMs', True )
scenario.changeSetting( artist, 'hide', 0 )
scenario.setIsActive( artist, True )

artist = scenario.add( 'Bubbles', ['I3Geometry', 'InIceDSTPulses', ] )
scenario.setIsActive( artist, False )
scenario.changeSetting( artist, 'colormap', I3TimeColorMap() )
scenario.changeSetting( artist, 'scale', 10 )
scenario.changeSetting( artist, 'power', 0.15 )
scenario.changeSetting( artist, 'static', PyQColor(255,0,255,255) )
scenario.changeSetting( artist, 'log10(delay/ns)', 6 ) #making change as suggested to fix color gradient.
scenario.changeSetting( artist, 'custom color window', '' )
scenario.setIsActive( artist, True )

artist = scenario.add( 'TextSummary', ['I3EventHeader', ] )
scenario.setIsActive( artist, False )
scenario.changeSetting( artist, 'short', True )
scenario.changeSetting( artist, 'font', PyQFont.fromString('Ubuntu,11,-1,5,50,0,0,0,0,0') )
scenario.changeSetting( artist, 'fontsize', 11 )
scenario.setOverlaySizeHints( artist, [OverlaySizeHint(10,10,201,55), ] )
scenario.setIsActive( artist, True )

window.gl.setCameraPivot(0.0, 0.0, 0.0)
window.gl.setCameraLoc(-747.6328735351562, 1301.1563720703125, 1024.01171875)
window.gl.setCameraOrientation(-0.8679603934288025, -0.49663251638412476, 0.0009470304357819259)
window.gl.cameraLock = False
window.gl.perspectiveView = True
window.gl.backgroundColor = PyQColor(80,80,80,255)
window.timeline.rangeFinder = "Default"
window.frame_filter.code = ""
window.activeView = 0


#######PREP I3 FILE######

app.files.selectFrame(0) #start by selecting 0th frame every new i3 file.
imageNum = int(app.files.nFrames) - 1 #use for ending index, subtract 1 bc nFrames doesn't start its counting at 0.

print("Total Number of Frames:", app.files.nFrames)
print("Total Number of Frames (including zero):", imageNum) #starts from 0.

app.files.nextMatchingFrame(icetray.I3Frame.DAQ) #Goes to first Q frame of i3 file.
starting_index = int(app.files.currentIndex) #saves the index of the first q frame in i3 file.
ending_index = int(app.files.nFrames) - starting_index

print("Starting index is:", starting_index)
print("Ending index is:", ending_index)
window.gl.backgroundColor = PyQColor(80,80,80,255) #sets background color (in this case to grey) in terms of RGB values.

#####LOOP THROUGH FRAMES IN CURRENTLY OPENED I3 FILE########
#Make sure steamshovel is opened and has correct displays selected and the camera is at a good starting point.

endframe = 15
#app.files.nFrames

for i in range(starting_index, endframe): #use nFrames because it is every frame, but print imageNum for number. USE 10 FOR BETA TEST
#app.files.nFrames, read end range
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
print("Total Number of Videos Expected:", ending_index)
window.close() #Close steamshovel when all frames have been turned into movies.
