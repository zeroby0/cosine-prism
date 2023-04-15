
from pathlib import Path

import numpy as np
import numpy.typing as npt

from matplotlib import pyplot as plt

import typing

from scipy.fft import dctn, idctn
from PIL import Image

from pathlib import Path

import quant_tables
import oklab


nd_uint8 = npt.NDArray[np.uint8]
nd_float64 = npt.NDArray[np.float64]

def image_lsrgb_to_oklab(im_r: nd_uint8, im_g: nd_uint8, im_b: nd_uint8) -> tuple[nd_float64, nd_float64, nd_float64]:
    # We convert the images to oklab, and then scale it the numbers
    # to be between 0 and 255
    l, m, s = oklab.lsrgb_to_oklab(im_r, im_g, im_b)

    l = (l - oklab.l_min) * 255 / oklab.l_range
    m = (m - oklab.m_min) * 255 / oklab.m_range
    s = (s - oklab.s_min) * 255 / oklab.s_range

    return (l, m, s)


def image_oklab_to_lsrgb(im_l: nd_float64, im_m: nd_float64, im_s: nd_float64) -> tuple[nd_uint8, nd_uint8, nd_uint8]:
    im_l = im_l * oklab.l_range / 255
    im_m = im_m * oklab.m_range / 255
    im_s = im_s * oklab.s_range / 255

    im_l = im_l + oklab.l_min
    im_m = im_m + oklab.m_min
    im_s = im_s + oklab.s_min

    return oklab.oklab_to_lsrgb(im_l, im_m, im_s)

def read_image_rgb(image_path: Path) -> tuple[nd_uint8, nd_uint8, nd_uint8]:
    image = np.asarray(
        Image.open(image_path).convert('RGB')
    )

    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    r = r[:r.shape[0] - r.shape[0]%8, :r.shape[1] - r.shape[1]%8]
    g = g[:g.shape[0] - g.shape[0]%8, :g.shape[1] - g.shape[1]%8]
    b = b[:b.shape[0] - b.shape[0]%8, :b.shape[1] - b.shape[1]%8]

    return r, g, b

def save_image_rgb(image_path: Path, im_r: nd_uint8, im_g: nd_uint8, im_b: nd_uint8):
    image_cropped = np.zeros([im_r.shape[0], im_r.shape[1], 3], dtype=np.uint8)

    image_cropped[:, :, 0] = im_r
    image_cropped[:, :, 1] = im_g
    image_cropped[:, :, 2] = im_b

    Image.fromarray(image_cropped).save(image_path)


image = 'wood'
size = 1024

image_path = Path(f'../images/{image}/{image}-{size}.png')

r, g, b = read_image_rgb(image_path)

l, m, s = image_lsrgb_to_oklab(r, g, b)


Image.fromarray(l.astype(np.uint8)).save('im_L.png')
Image.fromarray(m.astype(np.uint8)).save('im_M.png')
Image.fromarray(s.astype(np.uint8)).save('im_S.png')

Image.fromarray(s.astype(np.uint8) - m.astype(np.uint8)).save('im_S-M.png')