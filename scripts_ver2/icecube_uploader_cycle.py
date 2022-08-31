#icecube_uploader_cycle

import os
import sys
import h5py
import csv
import re
import pandas as pd
from os.path import join
from datetime import datetime
from run_config import Runconfig
import panoptes_client  # to interact with zooniverse
from panoptes_client import SubjectSet, Subject, Project, Panoptes

cut_val_lower = input("Input Lower Cut Val: ")
cut_val_greater = input("Input Greater Cut Val: ")

# df = pd.read_csv("run_config.csv")
# t = 0
# old_dir = df["directory"].values
# new_dir_lower = f"/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run21971/class_type_{str(t)}/less_than/cut_{str(cut_val_lower)}"
# new_dir_greater = f"/home/icecube/Desktop/eliz_zooniverse/icecubezooniverseproj_ver2/i3_files/Run21971/class_type_{t}/greater_than/cut_{cut_val_greater}"
#
# df['directory'] = df['directory'].replace({f'{old_dir}': f'{new_dir_lower}'})
#
# df.to_csv('run_config.csv')
# print(df['directory'])
