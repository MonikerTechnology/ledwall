from ledwall.color_utils import wheel, order_to_array
from ledwall.settings import settings


def rainbow_cycle(pixels, index, num_pixels):
    for i in range(num_pixels):
        pixel_index = (order_to_array(i) * 256 // num_pixels) + index
        pixels[order_to_array(i)] = wheel(pixel_index & 255) * settings.brightness
    pixels.show()

