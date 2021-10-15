from ledwall.color_utils import wheel


def rainbow_cycle(pixels, index, num_pixels):
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + index
        pixels[i] = wheel(pixel_index & 255)

