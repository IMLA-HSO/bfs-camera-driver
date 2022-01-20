import os

path = r'../flownet2-docker/flownet-Car/data'

# Read in the file
with open('both_output.txt', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('.png', '.flo')

# Write the file out again
with open('both_output.txt', 'w') as file:
  file.write(filedata)	
