
import numpy as np
import numpy.typing as npt

from matplotlib import pyplot as plt

import typing

from scipy.fft import dctn, idctn, dct, idct
from PIL import Image

from pathlib import Path

import quant_tables
import oklab

nd_uint8 = npt.NDArray[np.uint8]
nd_float64 = npt.NDArray[np.float64]


def pad_image_horiz(im):
    im_hpad = np.copy(im)

    im_hpad = np.hstack([
        im_hpad[:, 8:0:-1],
        im_hpad,
        im_hpad[:, -1:-9:-1]
    ])

    return im_hpad

def pad_image(im):
    im_hpad = pad_image_horiz(im)

    return pad_image_horiz(im_hpad.T).T

def mdct(x):
    N = x.shape[0]

    if N%4 != 0:
        raise ValueError("MDCT4 only defined for vectors of length multiple of four.")

    N4 = N // 4

    a = x[0*N4:1*N4]
    b = x[1*N4:2*N4]
    c = x[2*N4:3*N4]
    d = x[3*N4:4*N4]

    br = np.flip(b)
    cr = np.flip(c)

    return dct(np.hstack([-cr - d, a - br]), type=4, norm='ortho', orthogonalize=True) / 2


def imdct(y):
    N = y.shape[0] * 2

    if N%4 != 0:
        raise ValueError("IMDCT is only defined for vectors lengths multiple of two.")
    
    N4 = N // 4

    z = idct(y, type=4, norm='ortho', orthogonalize=True)

    z = np.hstack([z, -np.flip(z), -z]) * 2

    return z[N4:5*N//4]

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

def perform_mdct_horiz(im_any: nd_float64) -> nd_float64:
    im_any_hpad = pad_image_horiz(im_any)

    im_mdct = np.ones([im_any.shape[0], im_any.shape[1]+8])

    for i in range(im_any_hpad.shape[0]):
        for j in range(0, im_any_hpad.shape[1] - 8, 8):
            im_mdct[i][j:j+8] = mdct(im_any_hpad[i][j:j+16] * wfltr)

def perform_mdct(im_any: nd_float64) -> nd_float64:
    im_dct = np.zeros_like(im_any)

    # Do 8x8 DCT on image (in-place)
    for i in np.r_[:im_any.shape[0]:8]:
        for j in np.r_[:im_any.shape[1]:8]:
            im_dct[i:(i+8), j:(j+8)] = dctn(im_any[i:(i+8), j:(j+8)], axes=[0, 1], norm='ortho')
    
    return im_dct

def perform_imdct(im_any: nd_float64) -> nd_float64:
    im_dct = np.zeros_like(im_any)

    # Do 8x8 DCT on image (in-place)
    for i in np.r_[:im_any.shape[0]:8]:
        for j in np.r_[:im_any.shape[1]:8]:
            im_dct[i:(i+8), j:(j+8)] = idctn(im_any[i:(i+8), j:(j+8)], axes=[0, 1], norm='ortho')
    
    return im_dct

def quantise_dct(im_any: nd_float64, qtable = list[int]) -> nd_float64:
    im_quant = np.zeros_like(im_any)

    qtable = np.array(qtable).reshape((8, 8))

    for i in np.r_[:im_any.shape[0]:8]:
        for j in np.r_[:im_any.shape[1]:8]:
            im_quant[i:(i+8), j:(j+8)] = im_any[i:(i+8), j:(j+8)] / qtable
    
    return im_quant

def unquantise_dct(im_any: nd_uint8, qtable = list[int]) -> nd_float64:
    im_unquant = np.zeros_like(im_any, dtype=np.float64)

    qtable = np.array(qtable).reshape((8, 8))

    for i in np.r_[:im_any.shape[0]:8]:
        for j in np.r_[:im_any.shape[1]:8]:
            im_unquant[i:(i+8), j:(j+8)] = im_any[i:(i+8), j:(j+8)] * qtable
    
    return im_unquant

def split_quantised_dct(im_any: nd_float64, index_list: list[tuple[int, ...]]) -> dict[tuple[int, ...], nd_float64]:
    splits = {}
    for index in index_list:
        splits[index] = np.zeros([im_any.shape[0] // 8, im_any.shape[1] // 8, len(index)], dtype=np.float64)

    for i in np.r_[:im_any.shape[0]:8]:
        for j in np.r_[:im_any.shape[1]:8]:
            for index in index_list:
                splits[index][i//8, j//8, :] = im_any[i:(i+8), j:(j+8)].ravel()[list(index)]
    
    return splits

def write_to_disk(im_any, filepath: Path, dtype=np.int16):
    np.save(
        filepath,
        np.rint(im_any).astype(dtype)
    )

def array_to_img(im_any, filepath: Path):
    Image.fromarray(
        np.rint(
            im_any
        ).clip(0, 255).astype(np.uint8)
    ).save(filepath)

def mdct_static_oklab(image_path: Path) -> None:
    filename = image_path.name

    outputdir = Path(f'outputs/dct_static_oklab/{filename}/')
    outputdir.mkdir(exist_ok=True, parents=True)

    r, g, b = read_image_rgb(image_path)

    save_image_rgb(outputdir / 'original.png', r, g, b)

    l, m, s = image_lsrgb_to_oklab(r, g, b)

    qtable_l = 1 * quant_tables.dqt_90_dct_lum
    qtable_m = 4 * quant_tables.dqt_50_dct_lum
    qtable_s = 4 * quant_tables.dqt_50_dct_lum

    l_dct = perform_mdct(l)
    m_dct = perform_mdct(m)
    s_dct = perform_mdct(s)

    l_quant = quantise_dct(l_dct, qtable_l)
    m_quant = quantise_dct(m_dct, qtable_m)
    s_quant = quantise_dct(s_dct, qtable_s)

    # print(l.min())
    # print(l.max())
    # print(l_dct.min())
    # print(l_dct.max())
    # print(l_quant.min())
    # print(l_quant.max())

    # Round to uint8
    l_quant_uint8 = np.rint(l_quant)
    m_quant_uint8 = np.rint(m_quant)
    s_quant_uint8 = np.rint(s_quant)

    # l_quant_uint8 = l_quant
    # m_quant_uint8 = m_quant
    # s_quant_uint8 = s_quant

    l_unquant = unquantise_dct(l_quant_uint8, qtable_l)
    m_unquant = unquantise_dct(m_quant_uint8, qtable_m)
    s_unquant = unquantise_dct(s_quant_uint8, qtable_s)

    l_rec = perform_imdct(l_unquant)
    m_rec = perform_imdct(m_unquant)
    s_rec = perform_imdct(s_unquant)

    r_rec, g_rec, b_rec = image_oklab_to_lsrgb(l_rec, m_rec, s_rec)

    save_image_rgb(outputdir / 'recovered.png', r_rec, g_rec, b_rec)

    r_residue = r - r_rec
    g_residue = g - g_rec
    b_residue = b - b_rec

    l_residue = l - l_rec
    m_residue = m - m_rec
    s_residue = s - s_rec

    # print(r_residue.max())
    # print(g_residue.max())
    # print(b_residue.max())

    print(l_residue.min())
    print(m_residue.min())
    print(s_residue.min())

    a = np.zeros((r_residue.shape[0], r_residue.shape[1], 3), dtype=np.uint8)
    a[:, :, 0] = r_residue
    a[:, :, 1] = g_residue
    a[:, :, 2] = b_residue

    array_to_img(r_residue, outputdir / 'r_residue.png')
    array_to_img(a, outputdir / 'residue.png')

    dct_indices = [  0,  1,  8, 16,  9,  2,  3, 10, # ll
                    17, 24, 32, 25, 18, 11,  4,  5, # lh
                    12, 19, 26, 33, 40, 48, 41, 34, # lh
                    27, 20, 13,  6,  7, 14, 21, 28, # hl
                    35, 42, 49, 56, 57, 50, 43, 36, # hl
                    29, 22, 15, 23, 30, 37, 44, 51, # hh
                    58, 59, 52, 45, 38, 31, 39, 46, # hh
                    53, 60, 61, 54, 47, 55, 62, 63, # hh
    ]

    index_dc = tuple(dct_indices[0:1])
    index_ll = tuple(dct_indices[1:8])
    index_lh = tuple(dct_indices[8:16])
    index_hl = tuple(dct_indices[16:32])
    index_hh = tuple(dct_indices[32:64])

    l_splits = split_quantised_dct(l_quant, [index_dc, index_ll, index_lh, index_hl, index_hh])
    m_splits = split_quantised_dct(m_quant, [index_dc, index_ll, index_lh, index_hl, index_hh])
    s_splits = split_quantised_dct(s_quant, [index_dc, index_ll, index_lh, index_hl, index_hh])


    write_to_disk(
        np.hstack([
            l_splits[index_dc],
            m_splits[index_dc],
            s_splits[index_dc]
        ])
        , outputdir / 'dc.npy'
    )

    write_to_disk(
        np.hstack([
            l_splits[index_ll],
            m_splits[index_ll],
            s_splits[index_ll]
        ])
        , outputdir / 'll.npy'
    )

    write_to_disk(
        np.hstack([
            l_splits[index_lh],
            m_splits[index_lh],
            s_splits[index_lh]
        ])
        , outputdir / 'lh.npy'
    )

    write_to_disk(
        np.hstack([
            l_splits[index_hl],
            m_splits[index_hl],
            s_splits[index_hl]
        ])
        , outputdir / 'hl.npy'
    )

    write_to_disk(
        np.hstack([
            l_splits[index_hh],
            m_splits[index_hh],
            s_splits[index_hh]
        ])
        , outputdir / 'hh.npy'
    )

    write_to_disk(
        np.vstack([
            r_residue,
            g_residue,
            b_residue
        ])
        , outputdir / 'residue.npy',
        np.uint8
    )

    # r_residue_u50

    print(r_residue.size)

    print(np.sum(r_residue < 8))
    print(np.sum(r_residue > 247))

    print(np.sum(r_residue < 8) + np.sum(r_residue > 247) )

    # tbit = np.sum(r_residue < 4) + np.sum(r_residue > 251)

    # ebit = r_residue.size - tbit

    # print(tbit * 2 + ebit * 8)

    # print(tbit)

    print("Plotting")
    plt.hist(r_residue, 25)
    plt.savefig(outputdir / 'r_residue_hist.png')


    













    

