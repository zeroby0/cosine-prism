
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

def perform_dct(im_any: nd_float64) -> nd_float64:
    im_dct = np.zeros_like(im_any)

    # Do 8x8 DCT on image (in-place)
    for i in np.r_[:im_any.shape[0]:8]:
        for j in np.r_[:im_any.shape[1]:8]:
            im_dct[i:(i+8), j:(j+8)] = dctn(im_any[i:(i+8), j:(j+8)], axes=[0, 1], norm='ortho')
    
    return im_dct

def perform_idct(im_any: nd_float64) -> nd_float64:
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

def dct_static_oklab(image_path: Path) -> None:
    filename = image_path.name

    outputdir = Path(f'outputs/dct_static_oklab/{filename}/')
    outputdir.mkdir(exist_ok=True, parents=True)

    r, g, b = read_image_rgb(image_path)

    save_image_rgb(outputdir / 'original.png', r, g, b)

    l, m, s = image_lsrgb_to_oklab(r, g, b)

    qtable_l = 1 * quant_tables.dqt_90_dct_lum
    qtable_m = 4 * quant_tables.dqt_50_dct_lum
    qtable_s = 4 * quant_tables.dqt_50_dct_lum

    l_dct = perform_dct(l)
    m_dct = perform_dct(m)
    s_dct = perform_dct(s)

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

    l_rec = perform_idct(l_unquant)
    m_rec = perform_idct(m_unquant)
    s_rec = perform_idct(s_unquant)

    r_rec, g_rec, b_rec = image_oklab_to_lsrgb(l_rec, m_rec, s_rec)

    save_image_rgb(outputdir / 'recovered.png', r_rec, g_rec, b_rec)

    r_residue = r.astype(np.int8) - r_rec.astype(np.int8)
    g_residue = g.astype(np.int8) - g_rec.astype(np.int8)
    b_residue = b.astype(np.int8) - b_rec.astype(np.int8)

    l_residue = l.astype(np.int8) - l_rec.astype(np.int8)
    m_residue = m.astype(np.int8) - m_rec.astype(np.int8)
    s_residue = s.astype(np.int8) - s_rec.astype(np.int8)

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
    print(r_residue.dtype)

    print(np.sum(r_residue < 8))
    print(np.sum(r_residue > 247))

    print(np.sum(r_residue < 8) + np.sum(r_residue > 247) )

    # tbit = np.sum(r_residue < 4) + np.sum(r_residue > 251)

    # ebit = r_residue.size - tbit

    # print(tbit * 2 + ebit * 8)

    # print(tbit)

    print("Plotting")

    # print(r_residue.shape)

    plt.hist(r_residue.ravel(), 256, color='crimson')
    # plt.hist(g_residue.ravel(), 64, color='green')
    # plt.hist(b_residue.ravel(), 64, color='blue')
    plt.yscale('log')
    plt.title("Histogram of residue in the Red Channel of 1 Megapixel image")
    plt.ylabel("Number of pixels")
    plt.xlabel("Residue")
    plt.tight_layout()
    plt.savefig(outputdir / 'r_residue_hist.png', dpi=400)

    plt.cla()

    # plt.hist(r_residue.ravel(), 64, color='crimson')
    plt.hist(g_residue.ravel(), 256,  color='springgreen', cumulative=1)
    # plt.hist(b_residue.ravel(), 64, color='blue')
    plt.title("CDF of residue in the Green Channel of 1 Megapixel image")
    plt.ylabel("Cumulative probability")
    plt.xlabel("Residue")
    plt.tight_layout()
    plt.savefig(outputdir / 'g_residue_hist.png', dpi=400)

    # import seaborn as sns
    # sns.set_theme(style="whitegrid")

    # histogram = sns.histplot(
    #     r_residue.ravel(),
    #     binwidth=16
    # )

    # histogram.set(xlabel="Error", ylabel="Number of pixels", title="Histogram of error in the Red Channel")
    # histogram.figure.tight_layout()
    # histogram.figure.savefig(outputdir / "out.png", dpi=400) 

    













    

