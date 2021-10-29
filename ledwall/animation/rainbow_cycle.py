from ledwall.color_utils import wheel, order_to_array
from ledwall.settings import settings


def rainbow_cycle(pixels, index, num_pixels):
    for i in range(num_pixels):
        pixel_index = (order_to_array(i) * 256 // num_pixels) + index
        r, g, b, = wheel(pixel_index & 255)
        r *= settings.brightness
        g *= settings.brightness
        b *= settings.brightness
        pixels[order_to_array(i)] = (r, g, b)
    pixels.show()

