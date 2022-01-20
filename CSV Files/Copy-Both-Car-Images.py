import glob
import shutil
import os

src_dir = '../flownet2-docker/flownet-Car/data/car_both_data_flow'
dst_dir = '../flownet2-docker/flownet-Car/data/car_both_data_flow/car_both_optical'

for flofile in glob.iglob(os.path.join(src_dir, '*.png')):
    shutil.move(flofile, dst_dir)
