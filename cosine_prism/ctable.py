import math

# def getRGB(order):
#     th = ((order * math.pi) % 1 ) # is between 0 and 1

#     th = th * 2 * math.pi # scale it to 0 and 2 pi

#     r = math.cos(th)
#     g = math.cos(th + math.pi * 2/3)
#     b = math.cos(th + math.pi * 4/3)

#     # r, g, b are between -1 and 1, being outputs of cos
#     # make rgb be between 0 and 255
#     r = int((r + 1) * 255/2)
#     g = int((g + 1) * 255/2)
#     b = int((b + 1) * 255/2)

#     # Print as html/css hexcodes
#     # print(f'#{r:02x}{g:02x}{b:02x}')

#     return f'#{r:02x}{g:02x}{b:02x}'


def getCol(order):
    phibar = (math.sqrt(5) - 1)/2

    hue = ((order * phibar) % 1.0) * 2.0 * math.pi

    r = (math.cos(hue) + 0.5) / 1.5;
    g = (math.cos(hue - 2.0 * math.pi / 3.0) + 1.0) / 2.0;
    b = (math.cos(hue - 4.0 * math.pi / 3.0) + 1.0) / 2.0;

    # r, g, b are between -1 and 1, being outputs of cos
    # make rgb be between 0 and 255
    r = int((r + 1) * 255/2)
    g = int((g + 1) * 255/2)
    b = int((b + 1) * 255/2)

    # Print as html/css hexcodes
    # print(f'#{r:02x}{g:02x}{b:02x}')

    # return f'#{r:02x}{g:02x}{b:02x}'

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

    "DCT 2x2": 2,
    "DCT 4x4": 3,

    "DCT 16x16": 4,
    "DCT 32x32": 5,
    "DCT 64x64": 18,
    "DCT 128x128": 21,
    "DCT 256x256": 24,

    "DCT 4x8": 12,
    "DCT 8x4": 13,

    "DCT 8x16": 7,
    "DCT 8x32": 9,

    "DCT 16x8": 6,
    "DCT 16x32": 11,

    "DCT 32x8": 8,
    "DCT 32x16": 10,
    "DCT 32x64": 20,

    "DCT 64x32": 19,
    "DCT 64x128": 23,


    "DCT 128x64": 22,
    "DCT 128x256": 26,

    "DCT 256x128": 25,

    # All are 8x8. Should have very distinct colours
    "DCT 8x8": 0,
    "Hornuss": 1,
    "AFV0": 14, 
    "AFV1": 15, 
    "AFV2": 16, 
    "AFV3": 17, 
}




for transform in transforms:
    # print(transform, getCol(transforms[transform]))
    # print(
    #     '\definecolor{clr_vardct_' + "_".join(transform.split(' ')) + "}"
    #     + "{RGB}"
    #     + getCol(transforms[transform])
    # )


    print(
        "_".join(transform.split(' '))
        + " \t& "
        + transform
        + " \t& "
        + transform.split(' ')[-1]
    )
    # print(getCol(transforms[transform]))



# DCT 8x8 #ff3f3f
# Hornuss #cf01ad
# DCT 2x2 #6520f8
# DCT 4x4 #0d85ea
# DCT 16x16 #0ae68d
# DCT 32x32 #5efa25
# DCT 16x8 #cab300
# DCT 8x16 #fe4539
# DCT 32x8 #d502a6
# DCT 8x32 #6c1cf6
# DCT 32x16 #117eee
# DCT 16x32 #08e294
# DCT 4x8 #57fc2a
# DCT 8x4 #c4ba00
# AFV0 #fe4c33
# AFV1 #da049f
# AFV2 #7317f3
# AFV3 #1577f1
# DCT 64x64 #05dd9b
# DCT 64x32 #50fd30
# DCT 32x64 #bec000
# DCT 128x128 #fd522e
# DCT 128x64 #df0698
# DCT 64x128 #7a13f0
# DCT 256x256 #1970f4
# DCT 256x128 #03d8a1
# DCT 128x256 #4afe35