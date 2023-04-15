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

def lsrgb_to_xyb(r, g, b):
    xyb_bias = 0.00379307
    xyb_bias_cbrt = pow(xyb_bias, 1/3)

    # Convert from LSRGB to Linear LMS and the delinearise it with bias
    l = np.cbrt(0.30004500 * r + 0.62195876 * g + 0.07799694 * b + xyb_bias) - xyb_bias_cbrt
    m = np.cbrt(0.23006146 * r + 0.69200958 * g + 0.07799334 * b + xyb_bias) - xyb_bias_cbrt
    s = np.cbrt(0.24344419 * r + 0.20475293 * g + 0.55174833 * b + xyb_bias) - xyb_bias_cbrt

    x_ = 0.5 * l - 0.5 * m + 0.0 * s
    y_ = 0.5 * l + 0.5 * m + 0.0 * s
    b_ = 0.0 * l + 0.0 * m + 1.0 * s

    return (x_, y_, b_)

def xyb_to_lsrgb(x, y, b):
    l = L + 0.3963377774 * a + 0.2158037573 * b
    m = L - 0.1055613458 * a - 0.0638541728 * b
    s = L - 0.0894841775 * a - 1.2914855480 * b

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

