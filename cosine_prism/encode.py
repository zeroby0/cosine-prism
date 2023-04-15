from pathlib import Path

from dct_static import dct_static_oklab
# from mdct_static import mdct_static_oklab


image = 'earth'
size = 1024

image_path = Path(f'../images/{image}/{image}-{size}.png')

dct_static_oklab(image_path)
# mdct_static_oklab(image_path)