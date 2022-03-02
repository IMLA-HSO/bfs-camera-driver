import glob
import shutil
import os

# Source Directory
src_dir = '../flownet2-docker/flownet-Car/data/car_both_data_flow'

# Destination Directory
dst_dir = '../flownet2-docker/flownet-Car/data/car_both_data_flow/car_both_optical'

# Move data from source directory to destination directory
for flofile in glob.iglob(os.path.join(src_dir, '*.png')):
    shutil.move(flofile, dst_dir)
