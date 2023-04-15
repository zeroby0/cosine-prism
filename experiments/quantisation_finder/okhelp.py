import numpy as np
import colours
import oklab

# For OKLAB
m1_sx = np.matrix([
        [0.41241085, 0.35758457, 0.18045380],
        [0.21264934, 0.71516914, 0.07218152],
        [0.01933176, 0.11919486, 0.95039003],
])

m1_xo = np.matrix([
    [ 0.8189330101,  0.3618667424, -0.1288597137],
    [ 0.0329845436,  0.9293118715,  0.0361456387],
    [ 0.0482003018,  0.2643662691,  0.6338517070]
])

m1_so = np.matrix([
    [0.4122214708, 0.5363325363, 0.0514459929],
    [0.2119034982, 0.6806995451, 0.1073969566],
    [0.0883024619, 0.2817188376, 0.6299787005],
])

# print((m1_sx.T @ m1_xo.T).T)

# print((m1_so.T @ np.linalg.inv(m1_xo.T)).T)


# For XYB
m1_sx = np.matrix([
        [0.41241085, 0.35758457, 0.18045380],
        [0.21264934, 0.71516914, 0.07218152],
        [0.01933176, 0.11919486, 0.95039003],
])

m1_xl = np.matrix([
            [ 0.3739,  0.6896, -0.0413],
            [ 0.0792,  0.9286, -0.0035],
            [ 0.6212, -0.1027,  0.4704]
])

print((m1_sx.T @ m1_xl.T).T)


# rgb = np.array([
#     [10, 20, 30],
#     [10, 20, 30]
# ])

# print(np.inner(m1_so, rgb).T)

# xyz = np.inner(m1_sx, rgb).T

# print(np.asarray(xyz))

# okl = np.inner(m1_xo, xyz).T

# print(okl)




# b = np.inner(m1_xo, m1_sx)

# print(b)


# rgb = np.array([1, 2, 3])

# m1 = np.matrix([
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ])

# b = np.inner(m1, rgb)

# print(b)



# rgb = np.array([
#     [10, 20, 30],
#     [10, 20, 30]
# ])

# xyz = colours.SRGB.to_xyz(rgb)
# okl = colours.OKLAB.from_xyz(xyz)

# print(rgb)
# print(xyz)
# print(okl)

# okl2 = oklab.lsrgb_to_oklab(10, 20, 30)

# print(okl2)

# np.set_printoptions(precision=6, suppress=True)

# rgb = np.array([
#     [10, 20, 30]
# ])

# xyz = colours.SRGB.to_xyz(rgb)
# okl = colours.OKLAB.from_xyz(xyz)

# print(rgb)
# print(xyz)
# print(okl)

# xyz = colours.OKLAB.to_xyz(okl)
# rgb = colours.SRGB.from_xyz(xyz)

# print(xyz)
# print(rgb)


# okl = colours.OKLAB.from_xyz(xyz * 1000)

# print(okl)
# m1 = np.matrix([
#     [ 0.8189330101,  0.3618667424, -0.1288597137],
#     [ 0.0329845436,  0.9293118715,  0.0361456387],
#     [ 0.0482003018,  0.2643662691,  0.6338517070]
# ])

# m2 = np.matrix([
#     [ 0.2104542553,  0.7936177850, -0.0040720468],
#     [ 1.9779984951, -2.4285922050,  0.4505937099],
#     [ 0.0259040371,  0.7827717662, -0.8086757660]
# ])

# m1 = np.matrix([
#     [0.4124108464885388,   0.3575845678529519,  0.18045380393360833],
#     [0.21264934272065283,  0.7151691357059038,  0.07218152157344333],
#     [0.019331758429150258, 0.11919485595098397, 0.9503900340503373]
# ], dtype=np.float64)

# m2 = np.matrix([
# 	[ 3.240812398895283,    -1.5373084456298136,  -0.4985865229069666],
# 	[-0.9692430170086407,    1.8759663029085742,   0.04155503085668564],
# 	[ 0.055638398436112804, -0.20400746093241362,  1.0571295702861434]
# ], dtype=np.float64)

# print(m1)
# print(np.linalg.inv(m1))
# print(m2)

# print(np.allclose(m2, np.linalg.inv(m1)))