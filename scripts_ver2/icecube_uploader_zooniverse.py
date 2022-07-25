import os
import sys
import h5py
import csv
import re
from os.path import join
from datetime import datetime
from run_config import Runconfig
import panoptes_client  # to interact with zooniverse
from panoptes_client import SubjectSet, Subject, Project, Panoptes

"""This script is written in 64 bit Python 3.10, though it should run in any Python 3+ environment with the
following packages:
    - panoptes_client version 1.5
    - for Windows 64 bit and recent Mac OS's install python-magic-bin after the panoptes-client is installed.
    - For Windows 32 bit environments running on a AMD 64 bit processor, install python-magic-Win64
    after installing panoptes_client
    - a copy of the script run_config.py must be included in the working directory with this script
    - run_config.py requires the package cryptography at version 36.0+
    - the package regex version 2021.4.4 or later
    - h5py version 3.7

The first time this script is run, run_config.py will be called up to to build a file run_config.csv.
This will ask four questions - for the directory of where the project data files reside - generally where
you will keep this script and other files associated with the project (though it is not specifically used
for this script), your zooniverse username and zooniverse password, and finally the project slug for your
project.  The run_config.csv file will store your password in an encrypted format.  To retrieve the password
in plain text to send it to zooniverse the exact run_config.py file used to encrypt it is required  - anyone
with BOTH the run_config.csv and the exact run_config.py used to create it can retrieve the password, but
both the matching pair are needed.  Deleting the run_config.csv file will result in a new file being built
the next time this script is run, and run_config.py will be updated with with the new encryption key.

This script runs in an interactive mode, asking first for the full path and file name of the auxiliary .hd5 file
that matches the videos to upload. It then asks for the path to the top directory where the video files reside.

Next the script will ask for the name of the subject set to use, either creating it, or pausing
to acquire a list of existing subject if the subject set already exists.  This step queries zooniverse and is
slow. Generally one would not add new subjects to an existing set with many subjects (ie >10,000) already
uploaded unless it is to recover from an large upload that was interrupted - in which case just give it time....

Finally you are asked if you want a summary file build at the end of the upload process showing all the subjects
in the subject set with their zooniverse id and metadata in a format similar to the manifest.  This process
acquires the information directly from zooniverse and will be slow, but it shows exactly what is in zooniverse,
not what was intended...

Notes on the auxiliary .hd5 file:  As written, this script assumes the h5d file is a cut of the full I3Event file
and there will be a dataset ml_suite_classification in the root.  That dataset will have columns as follows:
Run, Event, SubEvent, SubEvent, Stream, exists, prediction_0000, prediction_0001, prediction_0002, prediction_0003,
prediction_0004, runtime_prediction, runtime_preprocess.
We use columns 0,1, and 2 as a key to a metadata dictionary for each row which includes key value pairs for columns
0, 1, and 5-9.

Notes on finding video files to upload:  The directory name where the video subdirectories are located as input
is used as the top directory for a search through that directory and all subdirectories of it in a full tree crawl.
All video files containing the string "compressed.mp4" are collected and the script will attempt to upload these
files.  The run and event are extracted from the file name.  If there is no corresponding metadata for that file
in the hd5 auxiliary file, then that video is no uploaded and a warning message is printed.

Once the subjects are prepared, the upload step occurs when the subject.save() is executed.  One can comment
out that line and the next subject_set.add(subject.id), and run the script as a "dry run".  The script will
report any issues just as if it is uploading (though much faster).   The script will report the number of files
uploaded, the number of subject previously uploaded in the subject set, and the number of failed uploads if any.
Once the dry run is error free, uncomment the two lines and repeat running the script.

If the upload stops at any time (usually connection issues with zooinverse), restart it with the same file,
directory, and subject set name and give it time to sort out what has and has not been uploaded to zooniverse.
This can be slow, but the script should resume where it ended off without duplicating subjects.  Even single
subjects can be deleted and re-uploaded if errors are found after the fact. Keep in mind it uses the original
filename to determine if a subject previously exists.

Finally when the upload is complete, the script builds the summary file if it was requested.  The summary
file is placed in the image directory under the name  'Uploaded_' + set_name + '_' + current date + ',csv'."""

reg_run = re.compile(r'run\d*_')
reg_event = re.compile(r'event\d*_')
reg_include = re.compile(r'compressed.mp4')


# run21971_event29359_index4_compressed.mp4
def get_files_in(folder):  # get list of files to upload
    file_listing = []
    for root, dirs, files in os.walk(folder):  # opens the directory and gets a list of all .mp4 files in it.
        for name in files:
            if reg_include.search(name):
                try:
                    run_ = reg_run.search(name).group(0)[3:]
                    event_ = reg_event.search(name).group(0)[5:]
                except AttributeError:
                    print('Could not extract run and event from file name', name)
                    continue
                metadata_key_ = run_ + event_ + '0'
                file_listing.append((metadata_key_, root, name))
    return file_listing


directory = Runconfig().working_directory

while True:  # interactive entry of the hd5 cut where the Run/Event metadata is acquired
    print('Enter the file name for the hd5 file cut that supports this upload')
    hd5_file = input('This file is assumed to reside in the working directory' + '\n')
    if os.path.isfile(join(directory, hd5_file)) and hd5_file[-4:] == '.hd5':
        break
    else:
        print('That entry is not an existing path and hd5 file')
        retry = input('Enter "y" to try again, any other key to exit' + '\n')
        if retry.lower() != 'y':
            quit()

while True:  # interactive entry of the directory where the video subdirectories are located, and a subject set name
    location = input('Enter the full path for the video directory' + '\n')
    if os.path.exists(location):
        break
    else:
        print('That entry is not a valid path for an existing directory')
        retry = input('Enter "y" to try again, any other key to exit' + '\n')
        if retry.lower() != 'y':
            quit()

set_name = input('Entry a name for the subject set to use or create.' + '\n')

#  test for the optional summary output
summary = False
if input('Enter "y" to save a summary file, any other key skip the summary' + '\n').lower() == 'y':
    summary = True

# build the metadata dictionary
f = h5py.File(join(directory, hd5_file), "r")
dataset = f['ml_suite_classification']
metadata = {}
for row in dataset[()]:
    metadata[str(row[0]) + '_' + str(row[1]) + '_' + str(row[2])] = {
        'Run': str(row[0]),
        'Event': str(row[1]),
        '#prediction_0000': str(row[5]),
        '#prediction_0001': str(row[6]),
        '#prediction_0002': str(row[7]),
        '#prediction_0003': str(row[8]),
        '#prediction_0004': str(row[9])
    }

# connect to zooniverse
Panoptes.connect(username=Runconfig().username, password=Runconfig().password)
project = Project.find(slug=Runconfig().project_slug)

file_list = get_files_in(location)  # go get the file list
number = len(file_list)
previous_subjects = []
try:
    # check if the subject set already exits:
    subject_set = SubjectSet.where(project_id=project.id, display_name=set_name).next()
    print('You have chosen to upload ', number, ' videos to an existing subject set', set_name)
    retry = input('Enter "n" to cancel this upload, any other key to continue' + '\n')
    if retry.lower() == 'n':
        quit()
    print('Checking for previously uploaded subjects, this could take a while!')
    for subject in subject_set.subjects:  # if the subject set does exist get a listing of what is in it
        previous_subjects.append(subject.metadata['Filename'])
except StopIteration:
    print('You have chosen to upload ', number, ' videos to an new subject set ', set_name)
    retry = input('Enter "n" to cancel this upload, any other key to continue' + '\n')
    if retry.lower() == 'n':
        quit()
    # if not, create a new subject set for the new data and link it to the project above
    subject_set = SubjectSet()
    subject_set.links.project = project
    subject_set.display_name = set_name
    subject_set.save()

print('Uploading subjects, this could take a while!')
videos_uploaded = 0
failed_upload = 0
previously_uploaded = 0

for metadata_key, path, original_file in file_list:  # loop through the file list
    # test if the file is already uploaded, if so skip it
    if original_file not in previous_subjects:
        # finally we are ready for the actual upload of the modified file:
        try:
            subject = Subject()
            subject.links.project = project
            print(original_file, 'uploading....')
            subject.add_location(join(path, original_file))
            subject.metadata['Filename'] = original_file
            try:
                subject.metadata.update(metadata[metadata_key])
            except KeyError:
                print('Could not find metadata for file', original_file, 'in .hd5 file')
                continue
            # nothing is actually uploaded to panoptes until the save is executed.
            # for testing without actually uploading anything comment out the following two lines
            subject.save()
            subject_set.add(subject.id)
            videos_uploaded += 1
        except panoptes_client.panoptes.PanoptesAPIException:
            print(str(sys.exc_info()[1]))
            print('An error occurred during the upload of', original_file)
            failed_upload += 1
    else:
        previously_uploaded += 1
print(videos_uploaded, 'videos uploaded')
print(videos_uploaded, 'videos successfully uploaded', previously_uploaded, 'subjects previously uploaded and',
      failed_upload, 'failed uploads.')

#  test for the optional summary output
if summary:
    print('Preparing summary file, please wait...')
    uploaded = 0
    with open(join(location, 'Uploaded_' + set_name + '_' + str(datetime.now())[0:10]
                             + '.csv'), 'w', newline='') as file:
        fieldnames = ['zoo_subject', 'Filename', 'Run', 'Event', '#prediction_0000',
                      '#prediction_0001', '#prediction_0002', '#prediction_0003', '#prediction_0004']

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        subject_set = SubjectSet.where(project_id=project.id, display_name=set_name).next()
        for subject in subject_set.subjects:
            uploaded += 1
            if (uploaded - 1) % 50 == 0:
                print('.', end='')
            new_line = subject.metadata
            new_line['zoo_subject'] = subject.id
            writer.writerow(subject.metadata)

        print('\n', uploaded, ' subjects found in the subject set, see the full list in  '
                              'Uploaded_' + set_name + '_' + str(datetime.now())[0:10] + '.csv')
