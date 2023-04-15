We need to find a good quantisation matrix for MDCT

We start with the quantisation matrix for normal dct, then we adjust it till we get to a target butteraugli distance.

After that, we use that matrix in MDCT and adjust till target butteraugli distance.

1.0 is visually lossless. 0.5-3.0 is the sane range.

Let's target 1.0. It's probably easier to reach it when quantising in XYB space, but XYB is on the back burner for now.

cjxl says distance 1.0 and quality 90 are default. And the quality is roughly equal to libjpegs quality, so JPEGs 90 quality qmatrix
is a good starting point.

----

Okay we have the quant tables for dct_lum quality 90 and 50.

Now we write a thing that applies DCT and quant and outputs a .png image.

Then we can see what butteraugli distance our qmats are producing.



