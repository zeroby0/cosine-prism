import numpy as np
import numpy.typing as npt

l_min = 0.0
l_max = 6.341325663998628
l_range = l_max - l_min

m_min = -1.4831572863679208
m_max = 1.7515803991801318
m_range = m_max - m_min

s_min = -1.9755014508238542
s_max = 1.2591954894854225
s_range = s_max - s_min


nd_uint8 = npt.NDArray[np.uint8]
nd_float64 = npt.NDArray[np.float64]

def lsrgb_to_oklab(r: nd_uint8, g: nd_uint8, b: nd_uint8) -> tuple[nd_float64, nd_float64, nd_float64]:
    l = np.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = np.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = np.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)

    l_ = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    m_ = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    s_ = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s

    return (l_, m_, s_)

def oklab_to_lsrgb(ok_L: nd_float64, ok_a: nd_float64, ok_b: nd_float64) -> tuple[nd_uint8, nd_uint8, nd_uint8]:
    l_ = ok_L + 0.3963377774 * ok_a + 0.2158037573 * ok_b
    m_ = ok_L - 0.1055613458 * ok_a - 0.0638541728 * ok_b
    s_ = ok_L - 0.0894841775 * ok_a - 1.2914855480 * ok_b

    l_ = np.power(l_, 3)
    m_ = np.power(m_, 3)
    s_ = np.power(s_, 3)

    r = +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    b = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_

    r = np.rint(r).clip(0, 255).astype(np.uint8)
    g = np.rint(g).clip(0, 255).astype(np.uint8)
    b = np.rint(b).clip(0, 255).astype(np.uint8)

    return r, g, b




# if __name__ == '__main__':
#     max_l = []
#     max_m = []
#     max_s = []

#     min_l = []
#     min_m = []
#     min_s = []

#     count = 0
#     for r in range(256):
#         for g in range(256):
#             l,m,s = lsrgb_to_oklab(
#                 np.ones(256) * r,
#                 np.ones(256) * g,
#                 np.arange(256)
#             )

#             # Find the max and min
#             max_l.append(np.max(l))
#             max_m.append(np.max(m))
#             max_s.append(np.max(s))

#             min_l.append(np.min(l))
#             min_m.append(np.min(m))
#             min_s.append(np.min(s))

#             # Verify that the RGB values didn't change

#             # Reduce the range count to 255 numbers
#             # We scale the numbers to 0-> 255, round to ints,
#             # And then scale it down to original range

#             # Scale numbers to 0->255
#             maxval = 255 * 8
#             l = (l - l_min) * maxval / l_range
#             m = (m - m_min) * maxval / m_range
#             s = (s - s_min) * maxval / s_range

#             # Round and clip them
#             l = np.rint(l).clip(0, maxval)
#             m = np.rint(m).clip(0, maxval)
#             s = np.rint(s).clip(0, maxval)

#             # Scale back to original range
#             l = (l * l_range / maxval) + l_min
#             m = (m * m_range / maxval) + m_min
#             s = (s * s_range / maxval) + s_min

#             r_, g_, b_ = oklab_to_lsrgb(l, m, s)

#             # print(b_ - np.arange(256))

#             assert np.allclose(r_, np.ones(256) * r)
#             assert np.allclose(g_, np.ones(256) * g)
#             assert np.allclose(b_, np.arange(256))

#             count += 1

#             print(count)

#     print(min(min_l), min(min_m), min(min_s))
#     print(max(max_l), max(max_m), max(max_s))


#     print(max(max_l) - min(min_l))
#     print(max(max_m) - min(min_m))
#     print(max(max_s) - min(min_s))

