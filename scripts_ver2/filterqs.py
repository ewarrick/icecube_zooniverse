#FILTER RETURNS Q FRAMES ONLY
#FILTER 2 OF 2.
#Imports modules
import numpy as np
from icecube import dataio, dataclasses, icetray
from I3Tray import *
import sys
import os
import argparse
import numpy as np

# def primary_cut(frame):
#     if frame['I3EventHeader'].sub_event_stream == 'NullSplit':
#         return False
#     elif frame['I3EventHeader'].sub_event_stream == 'InIceSplit':
#         return np.max(frame['ml_suite_classification'].values()[0:4]) <= 0.6

#ADD IN MAKE DIR FOR FILES? OR IS SAVING ALL TO ONE FOLDER FINE?

def dofilter(infile, outdir):
    drive, ipath =os.path.splitdrive(infile)
    path, ifn = os.path.split(ipath)
    infile_name = infile.split('/')[-1]
    tray = I3Tray()
    tray.Add('I3Reader', FilenameList=[infile])
    #tray.Add(primary_cut)
    tray.Add('I3MultiWriter', 'EventWriter',
    FileName= outdir+'daq_only-%04u_'+infile_name,
        Streams=[icetray.I3Frame.TrayInfo,
        icetray.I3Frame.Geometry,
        icetray.I3Frame.Calibration,
        icetray.I3Frame.DetectorStatus,
        icetray.I3Frame.DAQ,
        icetray.I3Frame.Stream('S')],
        SizeLimit = 2*10**6,)
    tray.AddModule('TrashCan','can')

    tray.Execute()
    tray.Finish()

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='Optional Arguments')
    parser.add_argument('--i',  metavar='infile', type=str)
    parser.add_argument('--o', metavar='outdir', help = 'output directory')
    args = parser.parse_args()
    infile = args.i
    outdir = args.o

    dofilter(infile,outdir)
