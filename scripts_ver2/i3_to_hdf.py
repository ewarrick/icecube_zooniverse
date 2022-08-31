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

def dofilter(infile, outdir):
    drive, ipath =os.path.splitdrive(infile)
    path, ifn = os.path.split(ipath)
    infile_name = infile.split('/')[-1]
    tray = I3Tray()
    tray.Add('I3Reader', FilenameList=[infile])
    tray.Add('I3Writer', 'EventWriter',
    FileName= infile_name,
        Streams=[icetray.I3Frame.TrayInfo,
        icetray.I3Frame.Geometry,
        icetray.I3Frame.Calibration,
        icetray.I3Frame.DetectorStatus,
        icetray.I3Frame.DAQ,
        icetray.I3Frame.Physics,
        icetray.I3Frame.Stream('S')],
        DropOrphanStreams=[icetray.I3Frame.DAQ])
    tray.AddSegment(I3HDFWriter, Output = infile+'.hd5', Keys = ['I3EventHeader','ml_suite_classification', 'NuGPrimary','PoleMuonLinefit', 'PoleMuonLinefitParams', 'PoleMuonLlhFitMuE', 'PoleMuonLlhFitFitParams', 'PoleMuonLlhFit'],SubEventStreams=['InIceSplit'])
    tray.AddModule('TrashCan','can')

    tray.Execute()
    tray.Finish()

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='Optional Arguments')
    parser.add_argument('--i',  dest='infile', type=str)
    parser.add_argument('--o', dest='outdir', help = 'output directory')
    # parser.add_argument('--cut_val', dest='cut_val', type=float, default = 0.6)
    # parser.add_argument('--greater_than',action='store_true', dest = 'greater_than') #if want less than don't include greater than
    # parser.add_argument('--class_type', type = int, default = 0, dest = 'class_type')
    args = parser.parse_args()
    infile = args.infile
    outdir = args.outdir

    dofilter(infile,outdir)
