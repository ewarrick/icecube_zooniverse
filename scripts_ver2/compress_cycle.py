#Handbrake compression cycle

import os
import subprocess
import argparse
import sys
#from icecube import dataio, dataclasses, icetray
import numpy as np
import glob
import ffmpy

run_id = str(21971)
scripts_directory = f'/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/scripts_ver2/'
directory = '/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run'+run_id+'/'

#class_type = input("Class type? ")
#greaterorless = input("greater or less? ")
cut_val_less = input("Input Lower Cut Value: ")
cut_val_greater = input("Input Greater Cut Value: ")

def compress(original_location, output_name):  # converts video container and reduces file size
    inp = {original_location: None}
    outp = {output_name: '-loglevel 8 -c:v libx264 -crf 26 -pix_fmt yuv420p -y'}
    # outp = {output_name: '-loglevel 8 -vf scale=640:480 -pix_fmt yuv420p -y'}
    ff = ffmpy.FFmpeg(inputs=inp, outputs=outp)
    return ff.run()

#os.mkdir(f'{directory}/compressed_videos') get videos to single directory

for t in range(0,5):
    film_files_less = glob.glob(f'{directory}class_type_{str(t)}/less_than/cut_{str(cut_val_less)}/Film*[!_compressed]/*.mp4', recursive = True)

    film_files_greater = glob.glob(f'{directory}class_type_{str(t)}/greater_than/cut_{str(cut_val_greater)}/Film*[!_compressed]/*.mp4', recursive = True)

    for file in film_files_less: #location of i3 files

        filename = os.path.basename(file)
        path_only = str(os.path.split(file)[0])
        name_only = os.path.split(file)[1]
        name_no_ext = str(os.path.splitext(name_only)[0])
        #v = f"{file}, {path_only}_compressed/{name_no_ext}_compressed.mp4"
        compress(file, path_only+'_compressed/'+name_no_ext+'compressed.mp4')

        #f"{file}, {path_only}_compressed/{name_no_ext}_compressed.mp4")
        #subprocess.call(f'HandBrakeCLI --preset-import-file {scripts_directory}ZooniverseCompression.json -i {file} -o {path_only}_compressed/{name_no_ext}_compressed.mp4', shell=True)

    for file_other in film_files_greater: #location of i3 files

        filename = os.path.basename(file_other)
        path_only = os.path.split(file_other)[0]
        name_only = os.path.split(file_other)[1]
        name_no_ext = os.path.splitext(name_only)[0]
        compress(file_other, path_only+'_compressed/'+name_no_ext+'_compressed.mp4')
        #f"{file_other}, {path_only}_compressed/{name_no_ext}_compressed.mp4")

    #     compress(f'-i {file} -o {path_only}_compressed/{name_no_ext}_compressed.mp4')
        #subprocess.call(f'HandBrakeCLI --preset-import-file {scripts_directory}ZooniverseCompression.json -i {file} -o {path_only}_compressed/{name_no_ext}_compressed.mp4', shell=True)
print("Done! :)")
