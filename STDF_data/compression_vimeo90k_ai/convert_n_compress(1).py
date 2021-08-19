import yaml
import os
import os.path as op


# load parameters
with open('option.yml', 'r') as fp:
    opts_dict = yaml.load(fp, Loader=yaml.FullLoader)

# PNG --> 7-frame YCbCr YUV444P
dataset_root = opts_dict['dataset_root']
os.system(f'python script/png2yuv.py {dataset_root}')

# generate video cfg
raw_dir = op.join(dataset_root, 'vimeo_septuplet_ycbcr')
os.system(f'python script/generate_video_cfg.py {raw_dir}')

# encode AI mode
os.system(f'python script/encode.py {raw_dir}')
