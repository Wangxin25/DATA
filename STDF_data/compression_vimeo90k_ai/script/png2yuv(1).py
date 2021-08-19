"""
7 png --> 1 yuv 444p video.
BGR --> YCbCr
"""
import os
import sys
import numpy as np
import os.path as op
import glob
from cv2 import cv2
import multiprocessing as mp


vimeo_root_dir = sys.argv[1]
sep_dir = op.join(vimeo_root_dir, 'vimeo_septuplet')
save_dir = op.join(vimeo_root_dir, 'vimeo_septuplet_ycbcr')
if not op.exists(save_dir):
    os.makedirs(save_dir)


def _read_n_write(seq):
    ycrcb_save_path = op.join(
            save_dir, 
            f"{seq.split('/')[-3]}_{seq.split('/')[-2]}.yuv"
            )
    fp = open(ycrcb_save_path, 'wb')
    png_list = sorted(glob.glob(op.join(seq, '*.png'))) 
    for png_path in png_list:
        bgr_img = cv2.imread(png_path)
        code = getattr(cv2, 'COLOR_BGR2YCrCb')
        ycrcb_img = cv2.cvtColor(bgr_img, code).astype(np.uint8)

        ycrcb_img[:, :, 0].tofile(fp)  # y
        ycrcb_img[:, :, 2].tofile(fp)  # cb (u)
        ycrcb_img[:, :, 1].tofile(fp)  # cr (v)
    fp.close()


class Counter():
    def __init__(self):
        self.count = 0


if __name__ == '__main__':
    pool = mp.Pool()  # default processes: cpu core num

    def _callback(x):
        counter.count += 1
        print(f'\r{counter.count}', end='')

    counter = Counter()
    seq_list_list = sorted(glob.glob(op.join(sep_dir, 'sequences', '*/')))
    for seq_list_dir in seq_list_list:
        seq_list = sorted(glob.glob(op.join(seq_list_dir, '*/')))
        for seq in seq_list:
            pool.apply_async(
                func=_read_n_write, 
                args=(seq,),
                callback=_callback,   # callback need input arg x
                )
    pool.close()
    pool.join()
    print('\n> done.')
