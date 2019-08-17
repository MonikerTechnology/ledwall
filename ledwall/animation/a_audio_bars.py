from audioprocessing import AudioProcessor
import ledwall.color_utils as tools


def audio_bars(t, random_values, audio_o: AudioProcessor, coordinates):
    """Compute the color of a given pixel.

    This function is run once per frame unlike the other animation functions.

    I swapped y and z so below is wrong
    coordinates = [(x, z, y), (x, z, y), (x, z, y) ...]


    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixe ls
    random_values: a list containing a constant random value for each pixel

    Returns an (r, g, b) tuple in the range 0-255

    """
    pixels = []

    # One level for each pixel that should be illuminated
    vol_levels = audio_o.max_calc_volume / 9
    x = 0
    y = 1

    # TODO Variable brightness for whole column based on volume
    # only color if higher than last time

    for coord in coordinates:

        this_pixel = (0, 0, 0)  # Pixel should be off if not called upon below

        # Highest pixel and diff color (but low y value)
        audio_channel_volume = audio_o.data_dict[coord[x]]['max_volume']
        more_than_last = audio_o.data_dict[coord[x]]['max_volume'] > audio_o.data_dict[coord[x]]['max_last']
        if audio_channel_volume > vol_levels * coord[y] and more_than_last:
            this_pixel = (250, 250, 250)

        # Rest of the bar
        if vol_levels * (coord[y] + 1) > audio_o.data_dict[coord[0]]['falling_max'] > vol_levels * coord[2]:
            this_pixel = (150, 15, 150)

        pixels.append(this_pixel)
    return pixels  # Returns a list of pixels











