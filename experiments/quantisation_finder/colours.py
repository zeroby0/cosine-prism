import numpy as np

class srgb():
    def to_xyz(rgb):
        # Linearise RGB
        rgb = rgb / 255

        index_eotf = rgb < 0.04045

        rgb[index_eotf] = rgb[index_eotf] / 12.92
        rgb[np.invert(index_eotf)] = np.power((rgb[np.invert(index_eotf)] + 0.055)/1.055, 2.4)

        # Convert to XYZ
        mat_srgb_to_xyz = np.matrix([
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041]
        ])

        xyz = np.inner(mat_srgb_to_xyz, rgb).T

        return xyz

    def from_xyz(xyz):
        # Convert to RGB
        mat_xyz_to_srgb = np.matrix([
            [ 3.2404542, -1.5371385, -0.4985314],
            [-0.9692660,  1.8760108,  0.0415560],
            [ 0.0556434, -0.2040259,  1.0572252]
        ])

        rgb = np.inner(mat_xyz_to_srgb, xyz).T

        rgb = np.asarray(rgb)

        # Unlinearise
        index_eotf = rgb < 0.0031308
        index_eotf_neg = np.invert(index_eotf)

        rgb[index_eotf] = rgb[index_eotf] * 12.92
        rgb[index_eotf_neg] = 1.055 * np.power(rgb[index_eotf_neg], 1/2.4) - 0.055

        return np.rint(rgb * 255)

class oklab():
    l_min = 0.0
    l_max = 6.341325663998628
    l_range = l_max - l_min

    m_min = -1.4831572863679208
    m_max = 1.7515803991801318
    m_range = m_max - m_min

    s_min = -1.9755014508238542
    s_max = 1.2591954894854225
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
        lmslin = np.inner(oklab.m1, xyz).T

        lms = np.cbrt(lmslin)

        return np.inner(oklab.m2, lms).T

    def to_xyz(lab):
        m1_inv = np.linalg.inv(oklab.m1)
        m2_inv = np.linalg.inv(oklab.m2)

        lms = np.inner(m2_inv, lab).T

        lmslin = np.power(lms, 3)

        return np.inner(m1_inv, lmslin).T

class xyb():
    l_min = 0.003753303963121508
    l_max = 0.1842533039631215
    l_range = l_max - l_min

    m_min = 0.005648415732957033
    m_max = 0.07784841573295703
    m_range = m_max - m_min

    s_min = 0.0008924336021469598
    s_max = 0.951392433602147
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


