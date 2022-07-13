Procedures for Building Subject Set for IceCube Zooniverse -- VERSION 2

1) Download desired DNN Classifier i3 file from Cobalt (currently I am using a file located at /data/sim/sim-new/scratch/rsnihur/new_processing_test/IceCube/2020/generated/neutrino-generator/21971/ML) by typing in your local terminal (check that your current local working directory is where you want to save the i3 file) 'scp username@data.icecube.wisc.edu:/path/to/file/[filename].i3.bz2 .' (replace username with your username and filename with the i3 filename)

	1a) The scripts you will be using might have specified directories within them, so make sure to change them to your desired directories. note to self: change to make them take arguments?
	1b) Make sure to initialize the icetray environment shell ('icerec') prior to running any scripts.
	1c) Make a directory for the run and store the i3 file there, then make subdirectories for the different class types in the style 'class_type_i' where i is 0, 1, 2, 3, and 4.  
	
2) Apply filters to i3 file by running the scipt 'filterpreds_cycle.py' (note: the i3 file name is a specified variable within the script, so make sure to change the variable name)
	2a) Input desired cut values. The script will now go through your i3 file and filter out by type (option 0 through 4) and specified cut values (less than will set the max prediction value to be less than or equal to the cut value and greater than will set the max prediction to be greater than or equal to the cut value). 
	2b) While it's doing that, the filter will also make an hdf file for each cut (this will be converted to a csv for the Zooniverse metadata manifest). After that, the i3 file will go through another filter that removes any frame that isn't a DAQ frame and splits that file into multiple files of a denoted size.
	2c) To edit the individual filters see the python scripts: 'fitlerqs.py' (filter for q frames) and 'filterforpreds_inicesplit.py' (filter for cut values and hdf file). 

3) Make movies using steamshovel by running the script 'steamshovel_cycle.py'. Again, directories are specified in the script, so check that they are correct prior to running. This will make videos only out of DAQ frames. 
	3a) The actual script that makes a set of movies from one i3 file is 'moviescript_steamshovel.py'. This script makes the different directories for the videos and sets the displays for steamshovel. If you want to change how many videos are made, change the endframe variable. 
	3b) GCD is located in the directory 'i3_files'. 
	
4) Compress the videos using the script 'compress_cycle.py'. 
	4a) You will be prompted to input the upper and lower cut values that you input into the filter script in step (2). It should cycle through all class types of events. 
	
5) Zooniverse stuff --> update
	5a) Depends on what Peter comes up with. I currently have a jupyter notebook that turns the hdf tables into a csv (see 'turnhdf_tocsv.ipynb'). 
	5b) Build manifest and upload using script from Peter?
	
	Peter's uploader: Uses run_config script and python package cryptography.
	To change main directory either delete the run_config.csv or edit it to go to a different directory. 
	input hd5 file name with extension, input directory where compressed videos of that cut are stored, input name of subject set (if using a name that is already in use subjects will upload to existing set without deleting prior uploads). Rerun on uploader on any folder where the save and add to zooniverse functions are commented out to make the updates manifest/uploader log. 
