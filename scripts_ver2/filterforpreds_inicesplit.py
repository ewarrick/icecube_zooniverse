#FILTER RETURNS PHYS AND Q FRAMES OF SPECIFIED PREDICTION VALUES AND INICESPLIT
#FILTER 1 OF 2.
#Imports modules
import numpy as np
from icecube import dataio, dataclasses, icetray
from I3Tray import *
import sys
import os
import argparse
import numpy as np
import pandas as pd
import csv

def primary_cut(frame):

    if frame['I3EventHeader'].sub_event_stream == 'NullSplit':
        return False
    elif frame['I3EventHeader'].sub_event_stream == 'InIceSplit':
        preds_raw = frame['ml_suite_classification'].values()[0:4]
        preds = np.argmax(preds_raw, axis=0)
        #mask stuff
        return np.max(frame['ml_suite_classification'].values()[0:4]) <= 0.6


# skim_pred = frame['ml_suite_classification'].values()[0]
# cascade_pred = frame['ml_suite_classification'].values()[1]
# tgtrack_pred = frame['ml_suite_classification'].values()[2]
# starttrack_pred = frame['ml_suite_classification'].values()[3]
# stoptrack_pred = frame['ml_suite_classification'].values()[4]

def dofilter(infile, outdir):
    drive, ipath =os.path.splitdrive(infile)
    path, ifn = os.path.split(ipath)
    infile_name = infile.split('/')[-1]
    tray = I3Tray()
    tray.Add('I3Reader', FilenameList=[infile])
    tray.Add(primary_cut)
    tray.Add('I3Writer', 'EventWriter',
    FileName= outdir+'filtered_preds_'+infile_name,
        Streams=[icetray.I3Frame.TrayInfo,
        icetray.I3Frame.Geometry,
        icetray.I3Frame.Calibration,
        icetray.I3Frame.DetectorStatus,
        icetray.I3Frame.DAQ,
        icetray.I3Frame.Physics, #delete
        icetray.I3Frame.Stream('S')],
        DropOrphanStreams=[icetray.I3Frame.DAQ]) #delete
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
