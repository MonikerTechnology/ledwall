from ledwall.color_utils import wheel
from time import perf_counter


def rainbow_cycle(pixels, index, num_pixels):
    start = perf_counter()
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + index
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()
    end = perf_counter()
    print(f"rainbow_cycle took {end - start}")

