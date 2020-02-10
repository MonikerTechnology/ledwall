from ledwall import color_utils
from ledwall.settings import Settings

Settings.__init__()

def pixel_color(t, coord, ii, n_pixels):
    """Compute the color of a given pixel.
    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels
    Returns an (r, g, b) tuple in the range 0-255
    """
    # make moving stripes for x, y, and z
    x, y, z = coord
    r = color_utils.cos(x, offset=t / 4, period=1, minn=0, maxx=0.7)
    g = color_utils.cos(y, offset=t / 4, period=1, minn=0, maxx=0.7)
    b = color_utils.cos(z, offset=t / 4, period=1, minn=0, maxx=0.7)
    r, g, b = color_utils.contrast((r, g, b), 0.5, 2)

    # make a moving white dot showing the order of the pixels in the layout file
    spark_ii = (t*80) % n_pixels
    spark_rad = 8
    spark_val = max(0, (spark_rad - color_utils.mod_dist(ii, spark_ii, n_pixels)) / spark_rad)
    spark_val = min(1, spark_val*2)
    r += spark_val
    g += spark_val
    b += spark_val

    # apply gamma curve
    # only do this on live leds, not in the simulator
    #r, g, b = color_utils.gamma((r, g, b), 2.2)

    return (r * 256 * Settings.brightness,
            g * 256 * Settings.brightness,
            b * 256 * Settings.brightness)
