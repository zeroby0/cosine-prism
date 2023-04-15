import numpy as np

l_min = 0.0
l_max = 6.341325663998628
l_range = l_max - l_min

m_min = -1.4831572863679208
m_max = 1.7515803991801318
m_range = m_max - m_min

s_min = -1.9755014508238542
s_max = 1.2591954894854225
s_range = s_max - s_min

def lsrgb_to_oklab(r, g, b):
    l = np.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = np.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = np.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)

    l_ = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    m_ = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    s_ = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s

    return (l_, m_, s_)

def oklab_to_lsrgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l_ = np.power(l_, 3)
    m_ = np.power(m_, 3)
    s_ = np.power(s_, 3)

    l = +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    m = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    s = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_

    return (l, m, s)


if __name__ == '__main__':
    max_l = []
    max_m = []
    max_s = []

    min_l = []
    min_m = []
    min_s = []

    count = 0
    for r in range(256):
        for g in range(256):
            l,m,s = lsrgb_to_oklab(
                np.ones(256) * r,
                np.ones(256) * g,
                np.arange(256)
            )

            max_l.append(np.max(l))
            max_m.append(np.max(m))
            max_s.append(np.max(s))

            min_l.append(np.min(l))
            min_m.append(np.min(m))
            min_s.append(np.min(s))

            count += 1

            print(count)

    print(min(min_l), min(min_m), min(min_s))
    print(max(max_l), max(max_m), max(max_s))


    print(max(max_l) - min(min_l))
    print(max(max_m) - min(min_m))
    print(max(max_s) - min(min_s))

