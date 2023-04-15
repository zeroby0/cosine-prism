// Unscaled values for kOpsinAbsorbanceBias
const kB0 = 0.96723368009523958;
const kB1 = kB0;
const kB2 = kB0;
const kScale = 255.0;
const kScaleR = 1.0;
const kScaleG = 1.0;
const kInvScaleR = 1.0;
const kInvScaleG = 1.0;

const kOpsinAbsorbanceBias = [
  kB0 / kScale,
  kB1 / kScale,
  kB2 / kScale,
];

// Parameters for opsin absorbance.
const kM02 = 0.078;
const kM00 = 0.30;
const kM01 = 1.0 - kM02 - kM00;

const kM12 = 0.078;
const kM10 = 0.23;
const kM11 = 1.0 - kM12 - kM10;

const kM20 = 0.24342268924547819;
const kM21 = 0.20476744424496821;
const kM22 = 1.0 - kM20 - kM21;

const kOpsinAbsorbanceMatrix = [
  kM00 / kScale, kM01 / kScale, kM02 / kScale, kM10 / kScale, kM11 / kScale,
  kM12 / kScale, kM20 / kScale, kM21 / kScale, kM22 / kScale,
];

// Must be the inverse matrix of kOpsinAbsorbanceMatrix and match the spec.
const kDefaultInverseOpsinAbsorbanceMatrix = [
  2813.04956,  -2516.07070, -41.9788641, -829.807582, 1126.78645,
  -41.9788641, -933.007078, 691.795377,  496.211701
];

const kNegOpsinAbsorbanceBiasRGB = [
  -kOpsinAbsorbanceBias[0], -kOpsinAbsorbanceBias[1],
  -kOpsinAbsorbanceBias[2], 255
];

const kNegOpsinAbsorbanceBiasCbrt = kNegOpsinAbsorbanceBiasRGB.map(c => Math.cbrt(c));

const premul_absorb = new Array(12).fill(0);
for (let i = 0; i < 9; i++) {
  premul_absorb[i] = kOpsinAbsorbanceMatrix[i];
}
for (let i = 0; i < 3; i++) {
  const neg_bias_cbrt = -Math.cbrt(kOpsinAbsorbanceBias[i]);
  premul_absorb[9 + i] = neg_bias_cbrt;
}

function OpsinAbsorbance (r, g, b) {
  const bias = kOpsinAbsorbanceBias;
  const m = premul_absorb;
  const mixed0 = MulAdd(m[0], r, MulAdd(m[1], g, MulAdd(m[2], b, bias[0])));
  const mixed1 = MulAdd(m[3], r, MulAdd(m[4], g, MulAdd(m[5], b, bias[1])));
  const mixed2 = MulAdd(m[6], r, MulAdd(m[7], g, MulAdd(m[8], b, bias[2])));
  return [
    mixed0,
    mixed1,
    mixed2
  ];
}

function NegMulAdd (a, b, c) {
  return -a * b + c;
}

function MulAdd (a, b, c) {
  return a * b + c;
}

function gammaToLinear (n) {
  return n <= 0.0404482362771082 ? n / 12.92 : Math.pow((n + 0.055) / 1.055, 2.4);
}

function linearToGamma (n) {
  return n <= 0.00313066844250063 ? n * 12.92 : 1.055 * Math.pow(n, 1 / 2.4) - 0.055;
}

function rgbToXYB (rgb) {
  const [ lR, lG, lB ] = rgb.map(n => 255 * gammaToLinear(n / 255));

  let [ mixed0, mixed1, mixed2 ] = OpsinAbsorbance(lR, lG, lB);

  // mixed should be non-negative even for wide-gamut, so clamp to zero.
  mixed0 = Math.max(0, mixed0);
  mixed1 = Math.max(0, mixed1);
  mixed2 = Math.max(0, mixed2);

  // CubeRootAndAdd
  mixed0 = Math.cbrt(mixed0) + premul_absorb[9];
  mixed1 = Math.cbrt(mixed1) + premul_absorb[10];
  mixed2 = Math.cbrt(mixed2) + premul_absorb[11];

  return LinearXybTransform(mixed0, mixed1, mixed2);
}

function LinearXybTransform (r, g, b) {
  return [
    0.5 * (r - g),
    0.5 * (r + g),
    b
  ];
}

function xybToRGB (xyb) {
  const [
    opsin_x,
    opsin_y,
    opsin_b
  ] = xyb;
  const inv_scale_x = kInvScaleR;
  const inv_scale_y = kInvScaleG;
  const neg_bias_r = kNegOpsinAbsorbanceBiasRGB[0];
  const neg_bias_g = kNegOpsinAbsorbanceBiasRGB[1];
  const neg_bias_b = kNegOpsinAbsorbanceBiasRGB[2];

  // Color space: XYB -> RGB
  let gamma_r = inv_scale_x * (opsin_y + opsin_x);
  let gamma_g = inv_scale_y * (opsin_y - opsin_x);
  let gamma_b = opsin_b;

  gamma_r -= kNegOpsinAbsorbanceBiasCbrt[0];
  gamma_g -= kNegOpsinAbsorbanceBiasCbrt[1];
  gamma_b -= kNegOpsinAbsorbanceBiasCbrt[2];

  // Undo gamma compression: linear = gamma^3 for efficiency.
  const gamma_r2 = gamma_r * gamma_r;
  const gamma_g2 = gamma_g * gamma_g;
  const gamma_b2 = gamma_b * gamma_b;
  const mixed_r = MulAdd(gamma_r2, gamma_r, neg_bias_r);
  const mixed_g = MulAdd(gamma_g2, gamma_g, neg_bias_g);
  const mixed_b = MulAdd(gamma_b2, gamma_b, neg_bias_b);

  const inverse_matrix = kDefaultInverseOpsinAbsorbanceMatrix;

  // Unmix (multiply by 3x3 inverse_matrix)
  let linear_r, linear_g, linear_b;
  linear_r = inverse_matrix[0] * mixed_r;
  linear_g = inverse_matrix[3] * mixed_r;
  linear_b = inverse_matrix[6] * mixed_r;
  linear_r = MulAdd(inverse_matrix[1], mixed_g, linear_r);
  linear_g = MulAdd(inverse_matrix[4], mixed_g, linear_g);
  linear_b = MulAdd(inverse_matrix[7], mixed_g, linear_b);
  linear_r = MulAdd(inverse_matrix[2], mixed_b, linear_r);
  linear_g = MulAdd(inverse_matrix[5], mixed_b, linear_g);
  linear_b = MulAdd(inverse_matrix[8], mixed_b, linear_b);
  return [
    Math.round(linearToGamma(linear_r / 255) * 255),
    Math.round(linearToGamma(linear_g / 255) * 255),
    Math.round(linearToGamma(linear_b / 255) * 255)
  ];
}

console.log(rgbToXYB([100, 20, 35]))