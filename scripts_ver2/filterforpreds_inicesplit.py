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
from icecube.hdfwriter import I3HDFWriter

def maxany_cut(frame,cut_val=0.6, greater_than=False):
    if frame['I3EventHeader'].sub_event_stream == 'NullSplit':
        return False
    elif frame['I3EventHeader'].sub_event_stream == 'InIceSplit':
        #preds_raw = frame['ml_suite_classification'].values()[0:4]
        #preds = np.argmax(preds_raw, axis=0)
        #mask stuff
        if greater_than:
            return np.max(frame['ml_suite_classification'].values()[0:5]) >= cut_val
        else:
            return np.max(frame['ml_suite_classification'].values()[0:5]) <= cut_val

def maxone_cut(frame,cut_val, greater_than,class_type):
    if frame['I3EventHeader'].sub_event_stream == 'NullSplit':
        return False
    elif frame['I3EventHeader'].sub_event_stream == 'InIceSplit':
        #preds_raw = frame['ml_suite_classification'].values()[0:4]
        #preds = np.argmax(preds_raw, axis=0)
        #mask stuff
        if (np.argmax(frame['ml_suite_classification'].values()[0:5],axis=0) == class_type):
            if greater_than:
                return frame['ml_suite_classification'].values()[class_type] >= cut_val
            else:
                return frame['ml_suite_classification'].values()[class_type] <= cut_val
        else:
            return False


# skim_pred = frame['ml_suite_classification'].values()[0]
# cascade_pred = frame['ml_suite_classification'].values()[1]
# tgtrack_pred = frame['ml_suite_classification'].values()[2]
# starttrack_pred = frame['ml_suite_classification'].values()[3]
# stoptrack_pred = frame['ml_suite_classification'].values()[4]

def dofilter(infile, outdir,cut_val,greater_than,class_type):
    if greater_than:
        save_dir = os.path.join(outdir,'class_type_{}'.format(class_type),'greater_than','cut_{}'.format(cut_val))
    else:
        save_dir = os.path.join(outdir,'class_type_{}'.format(class_type),'less_than','cut_{}'.format(cut_val))
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    drive, ipath =os.path.splitdrive(infile)
    path, ifn = os.path.split(ipath)
    infile_name = infile.split('/')[-1]
    tray = I3Tray()
    tray.Add('I3Reader', FilenameList=[infile])
    tray.AddModule(maxone_cut,cut_val=cut_val,greater_than=greater_than,class_type=class_type)
    tray.Add('I3Writer', 'EventWriter',
    FileName= save_dir+'/filtered_preds_'+infile_name,
        Streams=[icetray.I3Frame.TrayInfo,
        icetray.I3Frame.Geometry,
        icetray.I3Frame.Calibration,
        icetray.I3Frame.DetectorStatus,
        icetray.I3Frame.DAQ,
        icetray.I3Frame.Physics, #delete
        icetray.I3Frame.Stream('S')],
        DropOrphanStreams=[icetray.I3Frame.DAQ]) #delete
    tray.AddSegment(I3HDFWriter, Output = save_dir+'.hd5', Keys = ['I3EventHeader','ml_suite_classification', 'NuGPrimary','PoleMuonLinefit', 'PoleMuonLinefitParams', 'PoleMuonLlhFitMuE', 'PoleMuonLlhFitFitParams', 'PoleMuonLlhFit'],SubEventStreams=['InIceSplit'])
    tray.AddModule('TrashCan','can')

    tray.Execute()
    tray.Finish()

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='Optional Arguments')
    parser.add_argument('--i',  dest='infile', type=str)
    parser.add_argument('--o', dest='outdir', help = 'output directory')
    parser.add_argument('--cut_val', dest='cut_val', type=float, default = 0.6)
    parser.add_argument('--greater_than',action='store_true', dest = 'greater_than') #if want less than don't include greater than
    parser.add_argument('--class_type', type = int, default = 0, dest = 'class_type')
    args = parser.parse_args()
    infile = args.infile
    outdir = args.outdir

    dofilter(infile,outdir,args.cut_val,args.greater_than,args.class_type)
