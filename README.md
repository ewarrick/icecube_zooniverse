Procedures for Building Subject Set for IceCube Zooniverse

1) Download desired DNN Classifier i3 file from Cobalt (/data/sim/sim-new/scratch/rsnihur/new_processing_test/IceCube/2020/generated/neutrino-generator/21971/ML)
2) Apply filters to i3 file. 
	2a) Run i3 file through script "filterforpreds_inicesplit.py" -- cuts out events that do not have desired subeventstream and desired prediction value. 
		Result: returns new i3 file "filtered_preds[run_id].i3.bz2"
	2b) Run new i3 file created in 2a through a second filter script "filterqs.py" -- filters out P (physics) frames and splits i3 file into multiple i3 files of 		specified size limit. 
		Result: returns multiple i3 files made up of only DAQ frames with predictions under specified limit, where the size of the i3 file is determined in 			script. 
3) Open steamshovel with (any) i3 file (and GCD) and make sure desired displays are selected -- this is a sanity check to make sure that the videos will have actual data displayed. 
	3a) Make sure you close steamshovel and all loaded i3 frames by using the command "window.close()" in the steamshovel python shell. 
4) Open steamshovel again with desired i3 file and GCD file. 
	4a) Make sure that the first frame selected is frame 0 (should be a frame from the GCD). 
	4b) Within python shell, run execute function to start the script. (Check on folder organization system)
	4c) Check that all videos were made and that steamshovel didn't segfault (but it should close after all videos have been completed, there is a print statement that tells you the event and run ids of the video that was just made and then prints out the current frame index out of all frames. This is a good place to check)
	4d) Stills and videos are stored in numbered folders corresponding to what number i3 file you are working on **note to self: see if folders can have run_id in title. 
5) Check organization.
	5a) Make sure that the folders of videos and stills are where you want them.
	5b) Make a new folder where compressed videos will be stored. 
6) Open Handbrake.
	6a) File --> Open Source --> [select folder of videos, check preset selected for ZooniverseCompression, set distination for compressed videos, check preferences 
	for naming convention of compressed file] --> Queue --> Add Multiple --> [check Select All, make sure queue in upper right corner has a number next to it 
	representing the number of videos in the queue] --> Hit green Start button. 
	6b) Check that videos are being compressed into desired folder with desired naming convention and are under 1 MB in file size. 
7) Make CSV Manifest for Zooniverse.
8) Upload subject set and csv to Zooniverse. 
	8a) Workflow?
