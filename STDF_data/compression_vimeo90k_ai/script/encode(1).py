"""
chmod first.
"""
import os
import sys
import glob
import os.path as op
import multiprocessing as mp
from tqdm import tqdm


video_dir = sys.argv[1]
enc_path = 'TAppEncoderStatic'
enc_cfg_path = 'script/encoder_intra_main_rext_qp37.cfg' #'encoder_lowdelay_P_main.cfg'


def _compress(cmd, tmp_save_bit_path):
    os.system(cmd)
    return tmp_save_bit_path


def _callback(tmp_save_bit_path):
    os.remove(f'{tmp_save_bit_path}')
    pbar.update(1)


vid_lst = sorted(glob.glob(op.join(video_dir, '*.yuv')))
pbar = tqdm(total=len(vid_lst), ncols=80)


pool = mp.Pool()  # default processes: cpu core num
for idx_vid, vid_path in enumerate(vid_lst):
    vid_name = vid_path.split('/')[-1].split('.')[-2]
    vid_cfg_path = f'cache_video_cfg/{vid_name}.cfg'

    save_cmp_path = vid_path.replace('vimeo_septuplet_ycbcr', 'vimeo_septuplet_ycbcr_intra/qp37')
    save_log_path = save_cmp_path.replace('.yuv', '.txt')
    tmp_save_bit_path = save_cmp_path.replace('.yuv', '.bin')

    save_dir = op.dirname(save_cmp_path)
    if not op.exists(save_dir):
        os.makedirs(save_dir)

    cmd = (
        f'./{enc_path} -c {enc_cfg_path} -c {vid_cfg_path} -o ' 
        f'{save_cmp_path} -b {tmp_save_bit_path} >{save_log_path}'
        )  # sh ./ will cause error!

    pool.apply_async(
        func=_compress, 
        args=(cmd, tmp_save_bit_path, ),
        callback=_callback
        )
# end of all vids
pool.close()
pool.join()
pbar.close()
print("> done.")
