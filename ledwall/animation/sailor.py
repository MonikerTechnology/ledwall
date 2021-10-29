from ledwall import color_utils
from ledwall.settings import settings
import time


settings.__init__()


def sailor(t, coord, ii, n_pixels, random_values):
    """Compute the color of a given pixel.
    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    Returns an (r, g, b) tuple in the range 0-255
    """

#     # random persistant color per pixel
#     r = color_utils.remap(random_values[(ii+0)%n_pixels], 0, 1, 0.2, 1)
#     g = color_utils.remap(random_values[(ii+3)%n_pixels], 0, 1, 0.2, 1)
#     b = color_utils.remap(random_values[(ii+6)%n_pixels], 0, 1, 0.2, 1)

    # random assortment of a few colors per pixel: pink, cyan, white
    if random_values[ii] < 0.5:
        r, g, b = (1, 0.3, 0.8)
    elif random_values[ii] < 0.85:
        r, g, b = (0.4, 0.7, 1)
    else:
        r, g, b = (2, 0.6, 1.6)

    # twinkle occasional LEDs
    twinkle_speed = 0.07
    twinkle_density = 0.1
    twinkle = (random_values[ii]*7 + time.time()*twinkle_speed) % 1
    twinkle = abs(twinkle*2 - 1)
    twinkle = color_utils.remap(twinkle, 0, 1, -1/twinkle_density, 1.1)
    twinkle = color_utils.clamp(twinkle, -0.5, 1.1)
    twinkle **= 5
    twinkle *= color_utils.cos(t - ii/n_pixels, offset=0, period=7, minn=0.1, maxx=1.0) ** 20
    twinkle = color_utils.clamp(twinkle, -0.3, 1)
    r *= twinkle
    g *= twinkle
    b *= twinkle

    # apply gamma curve
    # only do this on live leds, not in the simulator
    r, g, b = color_utils.gamma((r, g, b), 2.2)

    return (r * 255 * settings.brightness,
            g * 255 * settings.brightness,
            b * 255 * settings.brightness)
