from ledwall.color_utils import wheel
from time import perf_counter


def rainbow_cycle(pixels, index, num_pixels):
    for i in range(num_pixels):
        start = perf_counter()
        pixel_index = (i * 256 // num_pixels) + index
        end = perf_counter()
        print(f"pixel index took {end - start}")
        start = perf_counter()
        pixels[i] = wheel(pixel_index & 255)
        end = perf_counter()
        print(f"pixels[i] took {end - start}")

