import glob
import shutil
import os

# Source Directory
src_dir = '../flownet2-docker/flownet-Car/data'

# Destination Director
dst_dir = '../flownet2-docker/flownet-Car/data/car_yellow_data_flo'

# Move data from source directory to destination directory
for flofile in glob.iglob(os.path.join(src_dir, '*.flo')):
    shutil.move(flofile, dst_dir)
