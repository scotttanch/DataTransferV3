import pyrealsense2.pyrealsense2 as rs
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Reoirent set a new origin for the system as well as clears the position lists.
# Position lists shouldn't need to be save between origins so I believe this is
# safe
def reorient(pipe):
	pipe.stop()
	pipe.start(cfg)
	return

# Survey function
def survey(x_pos,y_pos,z_pos):
	while(True):
		try:
			frames = pipe.wait_for_frames()
			pose = frames.get_pose_frame()
			if pose:
				#Get new position and rotation
				position = pose.get_pose_data().translation
				#If new position is some distance from the last position record it, change this later to record if
				#There is an input signal from the survey wheel
				trigger = True
				if trigger == True:
					x_pos.append(round(position.x*3.28084,2))
					y_pos.append(round(-position.z*3.28084,2))
					z_pos.append(round(position.y*3.28084,2))
					print(x_pos[-1],",",y_pos[-1],",",z_pos[-1])
					time.sleep(0.5)
		except KeyboardInterrupt:
			user_in = input("Stop Survey? [y/n]: ")
			if user_in =='y':
				break
	return x_pos,y_pos,z_pos

# Save function
def save_file(x,y,z):
	data = np.array([x,y,z])
	data = data.T
	file_name =  input("Enter file number: ")
	np.savetxt("/home/stanch/public/DZTs/FILE____"+file_name+".csv",data,delimiter=",")
	return

# Clear the memory
def clear_mem(x,y,z):
	x = []
	y = []
	z = []
	return x,y,z

# Initialization
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.pose)
pipe.start(cfg)

x_pos = []
y_pos = []
z_pos = []

# Main Loop
while True:
	os.system("clear -x")
	
	print("Realsesne Position Tracking")
	print("Reorient [1]")
	print("Record Survey Line [2]")
	print("Save Survey Line [3]")
	print("Exit [4]")
	if x_pos != []:
		print("A path exists in storage, save before continuing")
		selection = input("")
	if selection == "1":
		print("Reorienting...")
		reorient(pipe)
	if selection == "2":
		print("Begining Survey...")
		x_pos,y_pos,z_pos = survey(x_pos,y_pos,z_pos)
	if selection == "3":
		print("Entering Save Mode...")
		save_file(x_pos,y_pos,z_pos)
		x_pos,y_pos,z_pos = clear_mem(x_pos,y_pos,z_pos)
	if selection == "4":
		print("Exiting Program")
		break

# Clean up
pipe.stop()
sys.exit(0)
