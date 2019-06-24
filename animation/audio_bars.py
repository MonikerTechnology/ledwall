from audio_processing import AudioProcessor


def audio_bars(t, random_values, audio_o: AudioProcessor, coordinates):
    """Compute the color of a given pixel.

    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels
    random_values: a list containing a constant random value for each pixel

    Returns an (r, g, b) tuple in the range 0-255

    """
    pixels = []

    vol_levels = audio_o.max_calc_volume / 9
    # print(coordinates)
    for coord in coordinates:

        this_pixel = (0, 0, 0)
        # print(coord)
        if audio_o.data_dict[coord[0]]['max_volume'] > vol_levels * coord[2]:
            this_pixel = (255, 255, 0)
        if vol_levels * (coord[2] + 1) > audio_o.data_dict[coord[0]]['falling_max'] > vol_levels * coord[2]:
            this_pixel = (255, 255, 255)

        pixels.append(this_pixel)
    return pixels











