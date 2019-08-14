def start_up(t, coord, ii, n_pixels):
    """Compute the color of a given pixel.
    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels
    Returns an (r, g, b) tuple in the range 0-255
    """
    global position
    x, y, z = coord
    # print(coord)
    # print("position")
    # print(int(position))
    if (ii == 0):
        r = value[int(position)]
        g = value[int(position)]
        b = value[int(position)]
    elif (ii == 1 or ii == 29 or ii == 28):
        r = value[int(position)] * .7
        g = value[int(position)] * .5
        b = value[int(position)] * .5
    else:
        r = 0
        g = 0
        b = 0

    position += .01
    if (position > 499):
        position = 0

    # padXData = touchOSC.padXData
    # padYData = int(touchOSC.padYData * .65)
    # print padYData
    # print touchOSC.padYData

    # r,g,b = colorOSC

    # if x == padXData and z == padYData:
    # r,g,b = draw.circle(padXData,padYData, x, z,colorOSC)
    # draw.circle(5,5, x, z)

    return (r, g, b)
