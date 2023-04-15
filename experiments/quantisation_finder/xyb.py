import math


def cbrt(x):
    if x<0:
        print("Warn: cbrt, x less than 0", x)
        return -math.pow(-x, 1/3)

    return math.pow(x, 1/3)


# Unscaled values for kOpsinAbsorbanceBias
kB0 = 0.96723368009523958
kB1 = kB0
kB2 = kB0
kScale = 255.0
kScaleR = 1.0
kScaleG = 1.0
kInvScaleR = 1.0
kInvScaleG = 1.0

kOpsinAbsorbanceBias = [
    kB0 / kScale,
    kB1 / kScale,
    kB2 / kScale,
]

# Parameters for opsin absorbance.
kM02 = 0.078
kM00 = 0.30
kM01 = 1.0 - kM02 - kM00

kM12 = 0.078
kM10 = 0.23
kM11 = 1.0 - kM12 - kM10

kM20 = 0.24342268924547819
kM21 = 0.20476744424496821
kM22 = 1.0 - kM20 - kM21

kOpsinAbsorbanceMatrix = [
    kM00 / kScale, kM01 / kScale, kM02 / kScale, kM10 / kScale, kM11 / kScale,
    kM12 / kScale, kM20 / kScale, kM21 / kScale, kM22 / kScale,
]

# Must be the inverse matrix of kOpsinAbsorbanceMatrix and match the spec.
kDefaultInverseOpsinAbsorbanceMatrix = [
    2813.04956,  -2516.07070, -41.9788641, -829.807582, 1126.78645,
    -41.9788641, -933.007078, 691.795377,  496.211701
]

kNegOpsinAbsorbanceBiasRGB = [
    -kOpsinAbsorbanceBias[0], -kOpsinAbsorbanceBias[1],
    -kOpsinAbsorbanceBias[2], 255
]

kNegOpsinAbsorbanceBiasCbrt = [cbrt(i) for i in kNegOpsinAbsorbanceBiasRGB]

premul_absorb = [0] * 12
premul_absorb[0:9] = kOpsinAbsorbanceMatrix[0:9]
premul_absorb[9:] = [cbrt(i) for i in kOpsinAbsorbanceBias]

def NegMulAdd(a, b, c):
    return -a * b + c

def MulAdd(a, b, c):
    return a * b + c

def OpsinAbsorbance(r, g, b):
    bias = kOpsinAbsorbanceBias
    m = premul_absorb

    mixed0 = MulAdd(m[0], r, MulAdd(m[1], g, MulAdd(m[2], b, bias[0])))
    mixed1 = MulAdd(m[3], r, MulAdd(m[4], g, MulAdd(m[5], b, bias[1])))
    mixed2 = MulAdd(m[6], r, MulAdd(m[7], g, MulAdd(m[8], b, bias[2])))

    return [
        mixed0,
        mixed1,
        mixed2
    ]

def gammaToLinear(n):
    if n <= 0.0404482362771082:
        return n / 12.92
    else:
        return math.pow((n + 0.055) / 1.055, 2.4)

def linearToGamma(n):
    if n <= 0.00313066844250063:
        return n * 12.92
    else:
        return 1.055 * math.pow(n, 1 / 2.4) - 0.055


def LinearXybTransform(r, g, b):
    return [
        0.5 * (r - g),
        0.5 * (r + g),
        b
    ]

def rgbToXYB(rgb):
    lR, lG, lB = [ 255 * gammaToLinear(i / 255) for i in rgb]

    mixed0, mixed1, mixed2 = OpsinAbsorbance(lR, lG, lB)

    # mixed should be non-negative even for wide-gamut, so clamp to zero.
    if mixed0 < 0: mixed0 = 0
    if mixed1 < 0: mixed1 = 0
    if mixed2 < 0: mixed2 = 0

    # CubeRootAndAdd
    mixed0 = cbrt(mixed0) + premul_absorb[9]
    mixed1 = cbrt(mixed1) + premul_absorb[10]
    mixed2 = cbrt(mixed2) + premul_absorb[11]

    return LinearXybTransform(mixed0, mixed1, mixed2)

def xybToRGB(xyb):
    opsin_x, opsin_y, opsin_b = xyb

    inv_scale_x = kInvScaleR
    inv_scale_y = kInvScaleG

    neg_bias_r = kNegOpsinAbsorbanceBiasRGB[0]
    neg_bias_g = kNegOpsinAbsorbanceBiasRGB[1]
    neg_bias_b = kNegOpsinAbsorbanceBiasRGB[2]

    # Color space: XYB -> RGB
    gamma_r = inv_scale_x * (opsin_y + opsin_x)
    gamma_g = inv_scale_y * (opsin_y - opsin_x)
    gamma_b = opsin_b

    gamma_r -= kNegOpsinAbsorbanceBiasCbrt[0]
    gamma_g -= kNegOpsinAbsorbanceBiasCbrt[1]
    gamma_b -= kNegOpsinAbsorbanceBiasCbrt[2]

    # Undo gamma compression: linear = gamma^3 for efficiency.
    gamma_r2 = gamma_r * gamma_r
    gamma_g2 = gamma_g * gamma_g
    gamma_b2 = gamma_b * gamma_b
    mixed_r = MulAdd(gamma_r2, gamma_r, neg_bias_r)
    mixed_g = MulAdd(gamma_g2, gamma_g, neg_bias_g)
    mixed_b = MulAdd(gamma_b2, gamma_b, neg_bias_b)

    inverse_matrix = kDefaultInverseOpsinAbsorbanceMatrix

    # Unmix (multiply by 3x3 inverse_matrix)
    linear_r = inverse_matrix[0] * mixed_r
    linear_g = inverse_matrix[3] * mixed_r
    linear_b = inverse_matrix[6] * mixed_r
    linear_r = MulAdd(inverse_matrix[1], mixed_g, linear_r)
    linear_g = MulAdd(inverse_matrix[4], mixed_g, linear_g)
    linear_b = MulAdd(inverse_matrix[7], mixed_g, linear_b)
    linear_r = MulAdd(inverse_matrix[2], mixed_b, linear_r)
    linear_g = MulAdd(inverse_matrix[5], mixed_b, linear_g)
    linear_b = MulAdd(inverse_matrix[8], mixed_b, linear_b)

    return [
        round(linearToGamma(linear_r / 255) * 255),
        round(linearToGamma(linear_g / 255) * 255),
        round(linearToGamma(linear_b / 255) * 255)
    ]

if __name__ == '__main__':
    rgb = [100, 20, 35]

    xyb = rgbToXYB(rgb)

    print(xyb)
    print(xybToRGB(xyb))