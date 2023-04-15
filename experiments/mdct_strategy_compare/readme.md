We have three strategis to do MDCT on image so far.

The mdct4 method by that guy,
and the other method from the blog using dct4


Both of these seem to produce the same result, so we can ignore the mdct4 and use our dct4 based method.

Now there are two strategies to handle the edge cases. We can either reflect the image, or use our folding.


And then we wanna prove that the inner content is same independent of the strategy.
The strategy should only affect the edges of the data.

Okay wait, let's also kinda create the XYB and compare. It really might be slightly better for image compression.

