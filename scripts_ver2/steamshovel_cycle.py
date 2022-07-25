#DRAFT of script to cycle through running steamshovel.
#Will likely still have to initialize steamshovel locally first to check displays and camera.
#steamshovelfunction calling SCRIPT
import os
import subprocess
import argparse
import sys
from icecube import dataio, dataclasses, icetray
import numpy as np
#from icecube.shovelart import PyQColor

#still need to open a file and gcd manually to check displays.

#greaterorless = input("greater or less? ")
cut_val_lower = input("Input Lower Cut Val: ")
cut_val_greater = input("Input Greater Cut Val: ")
run_id = str(21971)
directory = f'/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run{run_id}/' #i3 files
gcd_file = f"/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/GeoCalibDetectorStatus_2012.56063_V1.i3.gz"
movie_script = f"/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/scripts_ver2/moviescript_steamshovel.py"

for t in range(0,5):
    indir_less = f"{directory}class_type_{t}/less_than/cut_{str(cut_val_lower)}/"
    indir_greater = f"{directory}class_type_{t}/greater_than/cut_{str(cut_val_greater)}/"
    for filename in os.listdir(indir_less):
        f = os.path.join(indir_less, filename)
        if filename.startswith('daq'):
            print("Filename is: ",f)
            subprocess.call(f"steamshovel {gcd_file} {f} --vanillaconsole --script {movie_script} --batch", shell = True)

    for filename_other in os.listdir(indir_greater):
        f1 = os.path.join(indir_greater, filename_other)
        if filename_other.startswith('daq'):
            print("Filename is: ",f)
            subprocess.call(f"steamshovel {gcd_file} {f1} --vanillaconsole --script {movie_script} --batch", shell = True)

subprocess.call(f"find {directory} -name "*.png" -delete")






# run_id = str(21971)
# directory = '/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run'+run_id+'/' #i3 files
# for filename in os.listdir(directory): #location of i3 files
#     f = os.path.join(directory, filename)
#     # checking if it is a file
#     if os.endswith('.i3.bz2'):
#         print("Filename is:",f)
#         subprocess.call("steamshovel /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/GeoCalibDetectorStatus_2012.56063_V1.i3.gz"+" "+f+" "+" --vanillaconsole --script /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/scripts_ver2/moviescript_steamshovel.py", shell = True) #run script, load frames, etc.
