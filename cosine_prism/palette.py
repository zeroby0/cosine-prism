palette = [
    (57,146,131),
    (147,230,183), 
    (27,81,29), 
    (67,226,109), 
    (141,25,147), 
    (197,213,240), 
    (31,65,150), 
    (236,159,231), 
    (97,59,79), 
    (32,216,253), 
    (7,77,101), 
    (167,214,78), 
    (206,19,101), 
    (48,151,46), 
    (232,79,225), 
    (71,149,224), 
    (43,25,217), 
    (240,210,126), 
    (124,68,14), 
    (253,143,47), 
    (187,25,10), 
    (248,163,149), 
    (89,121,254),
    (145,145,145),
    (147,230,183), 
    (27,81,29), 
    (67,226,109), 
]

def rgb_to_string(rgb):
    r, g, b = rgb

    r = (r * 2.0 / 255.0) - 1.0
    g = (g * 2.0 / 255.0) - 1.0
    b = (b * 2.0 / 255.0) - 1.0

    return r, g, b

    return f'({r:.8f}, {g:.8f}, {b:.8f})'

    return f'{{{r}, {g}, {b}}}'

transforms = {
    "DCT 8x8": 0,
    "Hornuss": 1,
    "DCT 2x2": 2,
    "DCT 4x4": 3,
    "DCT 16x16": 4,
    "DCT 32x32": 5,
    "DCT 16x8": 6,
    "DCT 8x16": 7,
    "DCT 32x8": 8,
    "DCT 8x32": 9,
    "DCT 32x16": 10,
    "DCT 16x32": 11,
    "DCT 4x8": 12,
    "DCT 8x4": 13,
    "AFV0": 14, 
    "AFV1": 15, 
    "AFV2": 16, 
    "AFV3": 17, 
    "DCT 64x64": 18,
    "DCT 64x32": 19,
    "DCT 32x64": 20,
    "DCT 128x128": 21,
    "DCT 128x64": 22,
    "DCT 64x128": 23,
    "DCT 256x256": 24,
    "DCT 256x128": 25,
    "DCT 128x256": 26,
}

a = []

for transform in transforms:
    # print(transform, getCol(transforms[transform]))
    c = rgb_to_string(
            palette[transforms[transform]]
        )[2]
    
    print(f'{c:0.08f}f')
    

    # print(
    #     '\definecolor{clr_vardct_' + "_".join(transform.split(' ')) + "}"
    #     + "{RGB}"
    #     + rgb_to_string(
    #         palette[transforms[transform]]
    #     )
    # )

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
