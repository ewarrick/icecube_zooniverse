#DRAFT of script to cycle through running steamshovel.
#Will likely still have to initialize steamshovel locally first to check displays and camera.
#steamshovelfunction calling SCRIPT
import os
import argparse
import sys
from icecube import icetray

directory = 'files' #i3 files
for filename in os.listdir(directory): #location of i3 files
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        os.system('steamshovel') #run script, load frames, etc.
