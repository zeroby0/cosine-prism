

function mat_vec_mul(m, v) {
    var result = [];
    for (row of m) {
        let sum = 0;
        for (let i = 0; i < row.length; i++) {
            sum += row[i] * v[i];
        }
        result.push(sum);
    }
    return result;
}

// Argument is in range 0..1
function srgb_eotf(u) {
    if (u < 0.04045) {
        return u / 12.92;
    } else {
        return Math.pow((u + 0.055) / 1.055, 2.4);
    }
}
function srgb_eotf_inv(u) {
    if (u < 0.0031308) {
        return u * 12.92;
    } else {
        return 1.055 * Math.pow(u, 1/2.4) - 0.055;
    }
}
// Source: Wikipedia sRGB article, rounded to 4 decimals
const SRGB_TO_XYZ = [
    [0.4124, 0.3576, 0.1805],
    [0.2126, 0.7152, 0.0722],
    [0.0193, 0.1192, 0.9505]
];
const XYZ_TO_SRGB = [
    [3.2410, -1.5374, -0.4986],
    [-0.9692, 1.8760, 0.0416],
    [0.0556, -0.2040, 1.0570]
];
// Color is sRGB with 0..255 range. Result is in D65 white point.
function sRGB_to_XYZ(rgb) {
    const rgblin = rgb.map(x => srgb_eotf(x / 255));
    return mat_vec_mul(SRGB_TO_XYZ, rgblin);
}

function XYZ_to_sRGB(xyz) {
    const rgblin = mat_vec_mul(XYZ_TO_SRGB, xyz);

    console.log("--------")
    console.log(rgblin)

    return rgblin.map(x => Math.round(255 * srgb_eotf_inv(x)));
}
// const SRGB = {"to_xyz": sRGB_to_XYZ, "from_xyz": XYZ_to_sRGB};


// From Oklab article, then some numpy. Note these are transposed. I'm
// not sure I have the conventions right, but it is giving the right
// answer.
const OKLAB_M1 = [
    [ 0.8189,  0.3619, -0.1289],
    [ 0.033 ,  0.9293,  0.0361],
    [ 0.0482,  0.2644,  0.6339]
];
const OKLAB_M2 = [
    [ 0.2105,  0.7936, -0.0041],
    [ 1.978 , -2.4286,  0.4506],
    [ 0.0259,  0.7828, -0.8087]
];
const OKLAB_INV_M1 = [
    [ 1.227 , -0.5578,  0.2813],
    [-0.0406,  1.1123, -0.0717],
    [-0.0764, -0.4215,  1.5862]
];
const OKLAB_INV_M2 = [
    [ 1.0   ,  0.3963,  0.2158],
    [ 1.0   , -0.1056, -0.0639],
    [ 1.0   , -0.0895, -1.2915]
];
function Oklab_to_XYZ(lab) {
    const lms = mat_vec_mul(OKLAB_INV_M2, lab);
    const lmslin = lms.map(x => x * x * x);
    return mat_vec_mul(OKLAB_INV_M1, lmslin);
}
function XYZ_to_Oklab(xyz) {
    const lmslin = mat_vec_mul(OKLAB_M1, xyz);
    const lms = lmslin.map(Math.cbrt);
    return mat_vec_mul(OKLAB_M2, lms);
}
const OKLAB = {"to_xyz": Oklab_to_XYZ, "from_xyz": XYZ_to_Oklab};




const XYB_XYZ_TO_LMS = [
    [ 0.3739,  0.6896, -0.0413],
    [ 0.0792,  0.9286, -0.0035],
    [ 0.6212, -0.1027,  0.4704]
];
const XYB_LMS_TO_XYB = [
    [ 0.5, -0.5, 0.0],
    [ 0.5, 0.5, 0.0],
    [ 0.0, 0.0, 1.0],
]
const XYB_LMS_TO_XYZ = [
    [ 2.7253, -1.9993,  0.2245],
    [-0.2462,  1.2585, -0.0122],
    [-3.6527,  2.9148,  1.8268]
];
const XYB_XYB_TO_LMS = [
    [ 1.0, 1.0, 0.0],
    [ -1.0, 1.0, 0.0],
    [ 0.0, 0.0, 1.0],
]

const XYB_BIAS = 0.00379307;
const XYB_BIAS_CBRT = Math.cbrt(XYB_BIAS);

function XYB_to_XYZ(lab) {
    const lms = mat_vec_mul(XYB_XYB_TO_LMS, lab);
    const lmslin = lms.map(x => Math.pow(x + XYB_BIAS_CBRT, 3) - XYB_BIAS);
    return mat_vec_mul(XYB_LMS_TO_XYZ, lmslin);
}
function XYZ_to_XYB(xyz) {
    const lmslin = mat_vec_mul(XYB_XYZ_TO_LMS, xyz);
    const lms = lmslin.map(x => Math.cbrt(x + XYB_BIAS) - XYB_BIAS_CBRT);
    return mat_vec_mul(XYB_LMS_TO_XYB, lms);
}



rgb = [100, 207, 255]

xyz = sRGB_to_XYZ(rgb)
okl = XYZ_to_Oklab(xyz)

console.log(rgb)
console.log(xyz)
console.log(okl)

xyz = Oklab_to_XYZ(okl)
rgb = XYZ_to_sRGB(xyz)

console.log(xyz)
console.log(rgb)

rgb = [100, 207, 255]


console.log("------------------------------")


xyz = sRGB_to_XYZ(rgb)
okl = XYZ_to_XYB(xyz)

console.log(rgb)
console.log(xyz)
console.log(okl)

xyz = XYB_to_XYZ(okl)
rgb = XYZ_to_sRGB(xyz)

console.log(xyz)
console.log(rgb)


// xyz = sRGB_to_XYZ(rgb)

// xyz = [0.00609674, 0.00658579, 0.01323281]

// okl = XYZ_to_Oklab(xyz)

// console.log(rgb)
// console.log(xyz)
// console.log(okl)
// rgb = [1, 2, 3]
// xyz = sRGB_to_XYZ(rgb)
// xyb = XYZ_to_sRGB(xyz)

// console.log(rgb)
// console.log(xyz)
// console.log(xyb)

// a = [100, 20, 35]
// b = [
//     [1, 2, 3],
//     [4, 5, 6],
//     [7, 8, 9]
// ]

// c = mat_vec_mul(b, a)

// console.log(c)




