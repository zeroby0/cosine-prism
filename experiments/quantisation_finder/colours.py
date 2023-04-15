import numpy as np

class RGB():
    m1 = np.matrix([
            [0.41241085, 0.35758457, 0.18045380],
            [0.21264934, 0.71516914, 0.07218152],
            [0.01933176, 0.11919486, 0.95039003],
    ])

    def to_xyz(rgb):
        # Linearise RGB
        rgb = rgb / 255

        index_eotf = rgb < 0.04045

        rgb[index_eotf] = rgb[index_eotf] / 12.92
        rgb[np.invert(index_eotf)] = np.power((rgb[np.invert(index_eotf)] + 0.055)/1.055, 2.4)

        # Convert to XYZ
        xyz = np.inner(RGB.m1, rgb).T

        return xyz

    def from_xyz(xyz):
        # Convert to RGB
        m1_inv = np.linalg.inv(RGB.m1)

        rgb = np.inner(m1_inv, xyz).T
        rgb = np.asarray(rgb)

        # Unlinearise
        index_eotf = rgb < 0.0031308
        index_eotf_neg = np.invert(index_eotf)

        rgb[index_eotf] = rgb[index_eotf] * 12.92
        rgb[index_eotf_neg] = 1.055 * np.power(rgb[index_eotf_neg], 1/2.4) - 0.055

        return np.rint(rgb * 255)


class SRGB():
    m1 = np.matrix([
        [ 0.4124373,  0.35762841, 0.18040431 ],
        [ 0.21263387, 0.7151556,  0.07221053 ],
        [ 0.01926261, 0.1189837,  0.95005365 ],
    ])

    def to_xyz(rgb):
        # Convert to XYZ
        xyz = np.inner(SRGB.m1, rgb).T

        return xyz

    def from_xyz(xyz):
        # Convert to RGB
        m1_inv = np.linalg.inv(SRGB.m1)

        rgb = np.inner(m1_inv, xyz).T

        return rgb

class OKLAB():
    l_min = 0.0
    l_max = 4.641581436619223
    l_range = l_max - l_min

    m_min = -1.085751505011899
    m_max = 1.2820558484960098
    m_range = m_max - m_min

    s_min = -1.4464140125449498
    s_max = 0.9212794820216286
    s_range = s_max - s_min

    m1 = np.matrix([
        [ 0.8189330101,  0.3618667424, -0.1288597137],
        [ 0.0329845436,  0.9293118715,  0.0361456387],
        [ 0.0482003018,  0.2643662691,  0.6338517070]
    ])

    m2 = np.matrix([
        [ 0.2104542553,  0.7936177850, -0.0040720468],
        [ 1.9779984951, -2.4285922050,  0.4505937099],
        [ 0.0259040371,  0.7827717662, -0.8086757660]
    ])

    def from_xyz(xyz):
        xyz = xyz
        lmslin = np.inner(OKLAB.m1, xyz).T

        lms = np.cbrt(lmslin)

        return np.inner(OKLAB.m2, lms).T

    def to_xyz(lab):
        m1_inv = np.linalg.inv(OKLAB.m1)
        m2_inv = np.linalg.inv(OKLAB.m2)

        lms = np.inner(m2_inv, lab).T

        lmslin = np.power(lms, 3)

        xyz = np.inner(m1_inv, lmslin).T
        return xyz

class XYB():
    l_min = -0.0153977681855616
    l_max = 0.0280965796012263
    l_range = l_max - l_min

    m_min = 0
    m_max = 0.8453226281191751
    m_range = m_max - m_min

    s_min = 0
    s_max = 0.8453139918529277
    s_range = s_max - s_min

    def from_xyz(xyz):
        mat_xyz_to_lms = np.matrix([
            [ 0.3739,  0.6896, -0.0413],
            [ 0.0792,  0.9286, -0.0035],
            [ 0.6212, -0.1027,  0.4704]
        ])

        mat_lms_to_xyb = np.matrix([
            [ 0.5, -0.5, 0.0],
            [ 0.5, 0.5, 0.0],
            [ 0.0, 0.0, 1.0],
        ])

        xyb_bias = 0.00379307
        xyb_bias_cbrt = pow(xyb_bias, 1/3)

        lmslin = np.inner(mat_xyz_to_lms, xyz).T
        
        lms = np.cbrt(lmslin + xyb_bias) - xyb_bias_cbrt

        return np.inner(mat_lms_to_xyb, lms).T

    def to_xyz(xyb):
        mat_lms_to_xyz = np.matrix([
            [ 2.7253, -1.9993,  0.2245],
            [-0.2462,  1.2585, -0.0122],
            [-3.6527,  2.9148,  1.8268]
        ])

        mat_xyb_to_lms = np.matrix([
            [ 1.0, 1.0, 0.0],
            [ -1.0, 1.0, 0.0],
            [ 0.0, 0.0, 1.0],
        ])


        xyb_bias = 0.00379307
        xyb_bias_cbrt = pow(xyb_bias, 1/3)

        lms = np.inner(mat_xyb_to_lms, xyb).T
        
        lmslin = np.power(lms + xyb_bias_cbrt, 3) - xyb_bias

        return np.inner(mat_lms_to_xyz, lmslin).T


