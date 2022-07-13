import os
import subprocess
import argparse
import sys
from icecube import dataio, dataclasses, icetray
import numpy as np

#change to function that takes arguments?????
run_id = str(21971)
directory = '/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run'+run_id+'/'
scripts = '/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/scripts_ver2/'
i3_file = 'classifier_DST_IC86.2020_NuMu.021971.000493.i3.bz2'
t=0
cut_val_less = input("Input desired less than cut value: ")
cut_val_greater = input("Input desired greater than cut value: ")
for t in range(0,5):
    subprocess.call(f"python3 {scripts}filterforpreds_inicesplit.py --i {directory}/{i3_file} --o {directory} --cut_val {str(cut_val_less)} --class_type {str(t)}", shell = True)
    subprocess.call(f"python3 {scripts}filterforpreds_inicesplit.py --i {directory}/{i3_file} --o {directory} --cut_val {str(cut_val_greater)} --greater_than --class_type {str(t)}", shell = True)
    subprocess.call(f"python3 {scripts}filterqs.py --i {directory}class_type_{str(t)}/less_than/cut_{str(cut_val_less)}/filtered_preds_{i3_file} --o {directory}class_type_{str(t)}/less_than/cut_{str(cut_val_less)}/", shell=True)
    subprocess.call(f"python3 {scripts}filterqs.py --i {directory}class_type_{str(t)}/greater_than/cut_{str(cut_val_greater)}/filtered_preds_{i3_file} --o {directory}class_type_{str(t)}/greater_than/cut_{str(cut_val_greater)}/", shell=True)

    #'python3 /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/scripts_ver2/filterforpreds_inicesplit.py --i /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run21971/classifier_DST_IC86.2020_NuMu.021971.000493.i3.bz2 --o /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run21971/ --cut_val'+' '+ str(cut_val_less)+' '+'--class_type'+' '+str(t), shell=True)
    #subprocess.call('python3 /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/scripts_ver2/filterforpreds_inicesplit.py --i /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run21971/classifier_DST_IC86.2020_NuMu.021971.000493.i3.bz2 --o /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run21971/ --cut_val'+' '+str(cut_val_greater)+' '+ '--greater_than --class_type'+' '+str(t), shell=True)
    #subprocess.call('python3 /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/scripts_ver2/filterqs.py --i' +' '+ directory+'class_type_'+str(t)+'/less_than/cut_'+str(cut_val_less)+'/*.bz2 --o' +' '+directory+'class_type_'+str(t)+' '+'/less_than/cut_'+str(cut_val_less)+'/', shell=True)
    #subprocess.call('python3 /home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/scripts_ver2/filterqs.py --i' +' '+ directory+'class_type_'+str(t)+'/greater_than/cut_'+str(cut_val_greater)+'/*.bz2 --o'+' '+directory+'class_type_'+str(t)+' '+'/greater_than/cut_'+str(cut_val_greater)+'/', shell=True)
    t+=1
