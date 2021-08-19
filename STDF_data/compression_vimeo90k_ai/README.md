Download Vimeo-90K dataset; convert PNG into 7-frame YCbCr YUV444P videos; and compress these videos under QP37, All Intra, HM16.5.

1. Download [vimeo_septuplet.zip](http://data.csail.mit.edu/tofu/dataset/vimeo_septuplet.zip).
2. Unzip and put it at `/xxx/Vimeo-90K/vimeo_septuplet/`.
3. Edit `dataset_root` at `option.yml` as `/xxx/Vimeo-90K/`.
4. `$ chmod +x TAppEncoderStatic`
5. `$ python convert_n_compress.py`

Please refer to [STDF-PyTorch](https://github.com/RyanXingQL/STDF-PyTorch) for more details.
