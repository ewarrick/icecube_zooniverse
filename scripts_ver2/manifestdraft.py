#Early stages of draft to make a manifest, mainly for practice.
import csv
import numpy as np
from icecube import dataio, dataclasses, icetray
from I3Tray import *
import sys
import os
import argparse
import numpy as np

with open('icecubezoomanifestdraft.csv', 'w', newline='') as f:
    fieldnames = ['column1','column2','column3']
    thewriter = csv.DictWriter(f, fieldnames=fieldnames)

    #thewriter.writerow(['col1','col2','col3'])
    thewriter.writeheader()

    thewriter.writerow({'column1' : 'one', 'column2' : 'two','column3' :'three'})
    #for i in range(1,100):
        #thewriter.writerow(['one','two','three'])
