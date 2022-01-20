import glob
import shutil
import os

src_dir = '../flownet2-docker/flownet-Car/data'
dst_dir = '../flownet2-docker/flownet-Car/data/car_red_data_flo'

for flofile in glob.iglob(os.path.join(src_dir, '*.flo')):
    shutil.move(flofile, dst_dir)
