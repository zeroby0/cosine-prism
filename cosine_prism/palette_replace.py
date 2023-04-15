original = [
    (255, 159, 159),
    (107, 177, 252),
    (177, 243, 133),
    (221, 128, 215),
    (86, 232, 213),
    (241, 193, 134),
    (147, 146, 252),
    (130, 254, 156),
    (249, 142, 180),
    (91, 199, 241),
    (206, 227, 127),
    (195, 129, 234),
    (96, 246, 191),
    (253, 171, 148),
    (121, 164, 254),
    (159, 250, 140),
    (234, 131, 202),
    (85, 220, 225),
    (230, 207, 129),
    (166, 137, 247),
    (115, 254, 169),
    (254, 152, 167),
    (100, 185, 248),
    (188, 238, 130),
    (212, 127, 223),
    (89, 238, 204),
    (247, 185, 139),
]

modified = [
    (57, 146, 131),
    (147, 230, 183),
    (27, 81, 29),
    (67, 226, 109),
    (141, 25, 147),
    (197, 213, 240),
    (31, 65, 150),
    (236, 159, 231),
    (97, 59, 79),
    (32, 216, 253),
    (7, 77, 101),
    (167, 214, 78),
    (206, 19, 101),
    (48, 151, 46),
    (232, 79, 225),
    (71, 149, 224),
    (43, 25, 217),
    (240, 210, 126),
    (124, 68, 14),
    (253, 143, 47),
    (187, 25, 10),
    (248, 163, 149),
    (89, 121, 254),
    (145, 145, 145),
    (147, 230, 183),
    (27, 81, 29),
    (67, 226, 109),
]

from pathlib import Path
from PIL import Image
import numpy as np

def read_image_rgb(image_path: Path):
    image = np.asarray(
        Image.open(image_path).convert('RGB')
    )

    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    r = r[:r.shape[0] - r.shape[0]%8, :r.shape[1] - r.shape[1]%8]
    g = g[:g.shape[0] - g.shape[0]%8, :g.shape[1] - g.shape[1]%8]
    b = b[:b.shape[0] - b.shape[0]%8, :b.shape[1] - b.shape[1]%8]

    return np.copy(r), np.copy(g), np.copy(b)

def save_image_rgb(image_path: Path, im_r, im_g, im_b):
    image_cropped = np.zeros([im_r.shape[0], im_r.shape[1], 3], dtype=np.uint8)

    image_cropped[:, :, 0] = im_r
    image_cropped[:, :, 1] = im_g
    image_cropped[:, :, 2] = im_b

    Image.fromarray(image_cropped).save(image_path)

image_path = Path('earth-vardct-old.png')

r, g, b = read_image_rgb(image_path)

count = 0
for triplet in original:
    index_r = r == triplet[0]
    index_g = g == triplet[1]
    index_b = b == triplet[2]

    index_rgb = index_r & index_g & index_b

    print(index_r)
    print(index_g)
    print(index_b)

    print(index_rgb)


    index_rgb = np.logical_and(index_r, index_g)

    r[index_rgb] = modified[count][0]
    g[index_rgb] = modified[count][1]
    b[index_rgb] = modified[count][2]


save_image_rgb(
    Path('modified.png'),
    r, g, b
)

