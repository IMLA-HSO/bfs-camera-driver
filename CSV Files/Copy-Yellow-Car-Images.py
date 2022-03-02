import glob
import shutil
import os

# Source Directory
src_dir = '/home/carreralab/Documents/CMEWS21/flownet2-docker/flownet-Car/data/car_yellow_data_flo'

# Destination Directory
dst_dir = '/home/carreralab/Documents/CMEWS21/flownet2-docker/flownet-Car/data/car_yellow_data_flo/car_yellow_optical_img'

# Move data from source directory to destination directory
for flofile in glob.iglob(os.path.join(src_dir, '*.png')):
    shutil.move(flofile, dst_dir)
