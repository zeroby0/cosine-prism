
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from pathlib import Path

dirpath = Path('outputs/dct_static_oklab/earth-1024.png/')

original = dirpath / 'original.png'
recovered = dirpath / 'rec-jxl.png'

image_original = np.asarray(
    Image.open(original).convert('RGB')
)

image_recovered = np.asarray(
    Image.open(recovered).convert('RGB')
)

r_orig = image_original[:, :, 0]
g_orig = image_original[:, :, 1]
b_orig = image_original[:, :, 2]

r_rec  = image_recovered[:, :, 0]
g_rec  = image_recovered[:, :, 1]
b_rec  = image_recovered[:, :, 2]

r = r_orig - r_rec
g = g_orig - g_rec
b = b_orig - b_rec

im_diff = np.zeros_like(image_original)

im_diff[:, :, 0] = r
im_diff[:, :, 1] = g
im_diff[:, :, 2] = b

Image.fromarray(im_diff).save(dirpath / 'imdiff.png')

print("Plotting")
plt.hist(r, 32)
plt.savefig(dirpath / 'r_imgdiff_hist.png')