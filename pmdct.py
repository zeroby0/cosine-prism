import numpy as np

from scipy.fft import dct, idct

def mdct(state, input, lenbits):
    rl = 2 ** (lenbits-1)

    print(f'rl={rl}')
    
    i = 0
    while i < rl//2:
        print(i)
        state[i] = -input[rl//2+i] - input[rl//2-i-1]
        state[rl//2+i] = state[rl+i] - state[rl+rl-i-1]
        i += 1

    i = 0
    while i < rl:
        state[rl+i]     = input[i]
        i += 1
    
    print(state)
    return state

state = [0, 0, 0, 0, 0, 0, 0, 0]
state = mdct(state, [1, 2, 3, 4], 4)
state = mdct(state, [5, 6, 7, 8], 4)


[
  16,  11,  10,  16,  24,  40,  51,  61,
  12,  12,  14,  19,  26,  58,  60,  55,
  14,  13,  16,  24,  40,  57,  69,  56,
  14,  17,  22,  29,  51,  87,  80,  62,
  18,  22,  37,  56,  68, 109, 103,  77,
  24,  35,  55,  64,  81, 104, 113,  92,
  49,  64,  78,  87, 103, 121, 120, 101,
  72,  92,  95,  98, 112, 100, 103,  99,
]