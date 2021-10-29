from ledwall import color_utils
from ledwall.settings import settings
import math

settings.__init__()


def raver(t, n_pixels):


    # how many sine wave cycles are squeezed into our n_pixels
    # 24 happens to create nice diagonal stripes on the wall layout
    freq_r = 24
    freq_g = 24
    freq_b = 24

    # how many seconds the color sine waves take to shift through a complete cycle
    speed_r = 7
    speed_g = -13
    speed_b = 19

    pixels = []
    for ii in range(n_pixels):
        pct = (ii / n_pixels)
        # diagonal black stripes
        pct_jittered = (pct * 77) % 37
        blackstripes = color_utils.cos(pct_jittered, offset=t*0.05, period=1, minn=-1.5, maxx=1.5)
        blackstripes_offset = color_utils.cos(t, offset=0.9, period=60, minn=-0.5, maxx=3)
        blackstripes = color_utils.clamp(blackstripes + blackstripes_offset, 0, 1)
        # 3 sine waves for r, g, b which are out of sync with each other
        r = blackstripes * color_utils.remap(math.cos((t/speed_r + pct*freq_r)*math.pi*2), -1, 1, 0, 256)
        g = blackstripes * color_utils.remap(math.cos((t/speed_g + pct*freq_g)*math.pi*2), -1, 1, 0, 256)
        b = blackstripes * color_utils.remap(math.cos((t/speed_b + pct*freq_b)*math.pi*2), -1, 1, 0, 256)
        pixels.append((r * 255 * settings.brightness,
                       g * 255 * settings.brightness,
                       b * 255 * settings.brightness))
    return pixels
