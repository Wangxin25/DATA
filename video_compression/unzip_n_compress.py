import os
import glob
import yaml
import os.path as op
import multiprocessing as mp


def _compress(cmd, tmp_save_bit_path):
    os.system(cmd)
    os.remove(f'{tmp_save_bit_path}')


def main():
    # load parameters
    with open('option.yml', 'r') as fp:
        opts_dict = yaml.load(fp)

    platform = opts_dict['system']
    assert platform in ['ubuntu', 'windows'], 'Not implemented.'
    dir_dataset = opts_dict['dir_dataset']
    qp = opts_dict['qp']

    for phase in ['test_18', 'train_108']:
        # ===== unzip ======
        print(f'unzip...')

        if platform == 'ubuntu':
            zip_name_pre = phase + '.z*'
            zip_name = phase + '.zip'
            print(f'\nunziping {zip_name}...')
            zip_path = op.join(dir_dataset, zip_name)
            target_path = dir_dataset  # inside: test_18/
            os.system(f'zip -s 0 {zip_path} --out unsplit.zip')
            os.system(f'unzip unsplit.zip -d {target_path}')
            os.remove('unsplit.zip')

        elif platform == 'windows':
            if not os.path.exists('..\\train_108\\'):
                print('> make sure you unzipped the train_108.zip manually!')
            if not os.path.exists('..\\test_18\\'):
                print('> make sure you unzipped the test_18.zip manually!')

        print('> done.')

        # === generate video configuration files ===
        print(f'\ngenerate cfg...')
        os.system(f'python scripts/generate_video_cfg.py {dir_dataset} {phase}')
        print('> done.')

        # ===== run ===== #
        print(f'\ncompress...')

        if platform == 'ubuntu':
            enc_path = 'TAppEncoderStatic'
        elif platform == 'windows':
            enc_path = 'TAppEncoder.exe'
        enc_cfg_path = op.join('encoder_cfg_LDP', f'encoder_LDP_QP{qp}.cfg')
        vid_lst = glob.glob(op.join(dir_dataset, phase, 'raw', '*.yuv'))
        pool = mp.Pool(8)  # default processes: cpu core num
        for idx_vid, vid_path in enumerate(vid_lst):
            vid_name = op.basename(vid_path).split('.')[-2]
            vid_cfg_path = op.join('video_cfg', f'{phase}', f'{vid_name}.cfg')
            if platform == 'ubuntu':
                save_cmp_path = vid_path.replace('raw', f'HM16.5_LDP/QP{qp}')
            elif platform == 'windows':
                save_cmp_path = vid_path.replace('raw', f'HM16.5_LDP\\QP{qp}')
            save_log_path = save_cmp_path.replace('.yuv', '.txt')
            tmp_save_bit_path = save_cmp_path.replace('.yuv', '.bin')

            save_dir = op.dirname(save_cmp_path)
            if not op.exists(save_dir):
                os.makedirs(save_dir)

            cmd = (
                f'{enc_path} -c {enc_cfg_path} -c {vid_cfg_path} -o ' 
                f'{save_cmp_path} -b {tmp_save_bit_path} >{save_log_path}'
            )  # sh ./ will cause error!

            if platform == 'ubuntu':
                cmd = './' + cmd

            print(f'\n{idx_vid + 1}/{len(vid_lst)}: compressing {vid_name}...')
            pool.apply_async(
                func=_compress, 
                args=(cmd, tmp_save_bit_path, ),
                callback=None
            )
        pool.close()
        pool.join()
        print("> done.")


if __name__ == "__main__":
    main()
