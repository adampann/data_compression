Project objective and requirements:
Write a basic JPEG-like compressor (and a corresponding decompressor) for gray-scale images that does a level adjustment (subtract 128 from each byte), performs the DCT on blocks, quantizes coefficients with the luminance quantization matrix suggested by the JPEG standard, represents the DC coefficients by differences, and then performs lossless compression using a separate utility.
Your algorithm should have two options for the block size, 8x8 and 16x16:
For 16x16 blocks, scale the quantization matrix up by a factor of 2 in each dimension by duplicating values. That is, assuming that the upper left hand corner has index (0,0) and the lower right corner has index (7,7), then entry (i,j) is duplicated to entries (2i,2j), (2i+1,2j), (2i, 2j+1), and (2i+1,2j+1) of the 16 by 16 quantization matrix.
For images that have a size that is not a multiple of your block size in one or both dimensions, pad with 0's up to the next multiple of the block size.

For the lossless program in the experiments your report use three compressors:
1. UNIX compress

2. UNIX gzip

3. Your compressor from Part 1 of this assignment.
Or, if you were unable to complete Part 1, use UNIX bzip.

Note: All three of compress, gzip, and bzip are available in a terminal window on a machine in the COSCI lounge.
To experiment with your program on the test data, you will need to be able to compare the quality of the decompressed image as compared to the original using the PSNR measure. You should make your own program to do this.