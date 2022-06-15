#TurnsI3 File in hdf5 table that can be read into pynb to analyze the data. 
import numpy as np
from icecube import icetray, dataio, dataclasses
from I3Tray import I3Tray
from icecube.hdfwriter import I3HDFWriter
from icecube import tableio
from icecube import millipede
#from icecube.hdfwriter import I3SimHDFWriter
#desc: makes i3 file into hdf5 table with specified keys.
tray = I3Tray()

outfile = '/home/icecube/Desktop/eliz_zooniverse/test.hd5'
filename = '/home/icecube/Desktop/eliz_zooniverse/classifier_DST_IC86.2020_NuMu.021971.000493.i3.bz2'

tray.AddModule('I3Reader', filename=filename) #nugprimary, eventheader, PoleMuonLinefit','PoleMuonLinefitParams', ml classification, weightdict
tray.AddSegment(I3HDFWriter, Output = outfile, Keys=['NuGPrimary','I3EventHeader', 'PoleMuonLinefit','PoleMuonLinefitParams','ml_suite_classification', 'I3MCWeightDict'], SubEventStreams=['InIceSplit'])
tray.Execute()
tray.Finish()
