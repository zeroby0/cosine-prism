import numpy as np

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

m1_sl = (m1_sx.T @ m1_xl.T).T

def lsrgb_to_oklab(rgb):
    m2_lx = np.matrix([
        [ 0.5, -0.5, 0.0],
        [ 0.5, 0.5, 0.0],
        [ 0.0, 0.0, 1.0],
    ])

    xyb_bias = 0.00379307
    xyb_bias_cbrt = pow(xyb_bias, 1/3)

    lmslin = np.inner(m1_sl, rgb).T

    lms = np.cbrt(lmslin + xyb_bias) - xyb_bias_cbrt

    return np.inner(m2_lx, lms).T