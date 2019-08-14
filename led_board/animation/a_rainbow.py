from led_board import color_utils
from led_board.__main__ import scale

def rainbow(t, coord, ii, n_pixels, random_values):
    """Compute the color of a given pixel.

    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels
    random_values: a list containing a constant random value for each pixel

    Returns an (r, g, b) tuple in the range 0-255

    """

    # make moving stripes for x, y, and z
    x, y, z = coord

    # Scale the x and z to match the original map file wall.json
    x = scale(x, (0, 14), (-0.7, 0.7))
    z = scale(z, (0, 8), (-0.4, 0.4))

    y += color_utils.cos(x + 0.2 * z, offset=0, period=1, minn=0, maxx=0.6)
    z += color_utils.cos(x, offset=0, period=1, minn=0, maxx=0.3)
    x += color_utils.cos(y + z, offset=0, period=1.5, minn=0, maxx=0.2)

    # rotate
    x, y, z = y, z, x

    # shift some of the pixels to a new xyz location
    # if ii % 17 == 0:
    #     x += ((ii*123)%5) / n_pixels * 32.12 + 0.1
    #     y += ((ii*137)%5) / n_pixels * 22.23 + 0.1
    #     z += ((ii*147)%7) / n_pixels * 44.34 + 0.1

    # make x, y, z -> r, g, b sine waves
    r = color_utils.cos(x, offset=t / 4, period=2, minn=0, maxx=1)
    g = color_utils.cos(y, offset=t / 4, period=2, minn=0, maxx=1)
    b = color_utils.cos(z, offset=t / 4, period=2, minn=0, maxx=1)
    r, g, b = color_utils.contrast((r, g, b), 0.5, 1.5)
    # r, g, b = color_utils.clip_black_by_luminance((r, g, b), 0.5)
    #
    # # shift the color of a few outliers
    # if random_values[ii] < 0.03:
    #     r, g, b = b, g, r

    # black out regions
    r2 = color_utils.cos(x, offset=t / 10 + 12.345, period=3, minn=0, maxx=1)
    g2 = color_utils.cos(y, offset=t / 10 + 24.536, period=3, minn=0, maxx=1)
    b2 = color_utils.cos(z, offset=t / 10 + 34.675, period=3, minn=0, maxx=1)
    clampdown = (r2 + g2 + b2) / 2
    clampdown = color_utils.remap(clampdown, 0.8, 0.9, 0, 1)
    clampdown = color_utils.clamp(clampdown, 0, 1)
    r *= clampdown
    g *= clampdown
    b *= clampdown

    # color scheme: fade towards blue-and-orange
    # g = (r+b) / 2
    g = g * 0.6 + ((r + b) / 2) * 0.4

    # apply gamma curve
    # only do this on live leds, not in the simulator
    r, g, b = color_utils.gamma((r, g, b), 2.2)

    return (
    r * 250 * HTTPserver.redMultiplier, g * 250 * HTTPserver.greenMultiplier, b * 250 * HTTPserver.blueMultiplier)