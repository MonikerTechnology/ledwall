#!/usr/bin/env python

"""Helper functions to make color manipulations easier."""

from __future__ import division
import math
from typing import Tuple


def get_cord(pixel: int, width=15) -> Tuple[int, int]:
    """
    pixel: Actual index of pixel
    """
    column = pixel % width
    row = int(pixel / width)
    if row in [1, 4, 7]:
        column = width - column - 1
    return row, column


def get_pos(x, y, width=15):
    if x in [1, 4, 7]:
        y = width - y - 1
    return (x * 15) + y


# def order_to_array(num, width=15):
#     row = int(num / width)
#     column = num % width
#     if row in [1, 4, 7]:
#         column = width - column - 1
#     return (row * width) + column


def order_to_array(pos: int, width=15) -> int:
    """
    pos: Index of where the pixel would be if the strip was in order

    return: Actual index
    """
    row = int(pos / width)
    column = pos % width
    if row in [3, 4, 5]:
        column = width - column - 1
    return (row * width) + column


def array_to_order(num, width=15):
    pass


def inc_counter(pos, greatest=255):
    if pos < greatest:
        return pos + 1
    return 0


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)


def fade_pixel(last_rgb: tuple, target_rgb: tuple) -> tuple:
    """Single pixel"""
    out_rgb = list()
    for last, target in zip(last_rgb, target_rgb):
        out_rgb.append(color_to_target(last, target))
    return tuple(out_rgb)


def color_to_target(last, target, rate=8):
    if last == target:
        return target
    if abs(last - target) < rate:
        return target
    if target > last:
        return last + rate
    return last - rate


def remap(x, oldmin, oldmax, newmin, newmax):
    """Remap the float x from the range oldmin-oldmax to the range newmin-newmax

    Does not clamp values that exceed min or max.
    For example, to make a sine wave that goes between 0 and 256:
        remap(math.sin(time.time()), -1, 1, 0, 256)

    """
    zero_to_one = (x-oldmin) / (oldmax-oldmin)
    return zero_to_one*(newmax-newmin) + newmin

def clamp(x, minn, maxx):
    """Restrict the float x to the range minn-maxx."""
    return max(minn, min(maxx, x))

def cos(x, offset=0, period=1, minn=0, maxx=1):
    """A cosine curve scaled to fit in a 0-1 range and 0-1 domain by default.

    offset: how much to slide the curve across the domain (should be 0-1)
    period: the length of one wave
    minn, maxx: the output range

    """
    value = math.cos((x/period - offset) * math.pi * 2) / 2 + 0.5
    return value*(maxx-minn) + minn

def contrast(color, center, mult):
    """Expand the color values by a factor of mult around the pivot value of center.

    color: an (r, g, b) tuple
    center: a float -- the fixed point
    mult: a float -- expand or contract the values around the center point

    """
    r, g, b = color
    r = (r - center) * mult + center
    g = (g - center) * mult + center
    b = (b - center) * mult + center
    return (r, g, b)

def clip_black_by_luminance(color, threshold):
    """If the color's luminance is less than threshold, replace it with black.
    
    color: an (r, g, b) tuple
    threshold: a float

    """
    r, g, b = color
    if r+g+b < threshold*3:
        return (0, 0, 0)
    return (r, g, b)

def clip_black_by_channels(color, threshold):
    """Replace any individual r, g, or b value less than threshold with 0.

    color: an (r, g, b) tuple
    threshold: a float

    """
    r, g, b = color
    if r < threshold: r = 0
    if g < threshold: g = 0
    if b < threshold: b = 0
    return (r, g, b)

def mod_dist(a, b, n):
    """Return the distance between floats a and b, modulo n.

    The result is always non-negative.
    For example, thinking of a clock:
    mod_dist(11, 1, 12) == 2 because you can "wrap around".

    """
    return min((a-b) % n, (b-a) % n)

def gamma(color, gamma):
    """Apply a gamma curve to the color.  The color values should be in the range 0-1."""
    r, g, b = color
    return (max(r, 0) ** gamma, max(g, 0) ** gamma, max(b, 0) ** gamma)

