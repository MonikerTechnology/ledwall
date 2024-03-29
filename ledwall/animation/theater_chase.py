from ledwall.color_utils import order_to_array, wheel
from time import sleep, perf_counter
from ledwall.settings import settings

def theaterChaseRainbow(pixels, counter_a, counter_b, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    # start = perf_counter()
    # for counter_b in range(3):
    for i in range(0, pixels.n, 3):
        r, g, b, = wheel((i + counter_a) % 255)
        r *= settings.brightness
        g *= settings.brightness
        b *= settings.brightness
        pixels[order_to_array(i + counter_b)] = (r, g, b)
    # end = perf_counter()
    # print(f"Picking values took: {end-start}s")
    # start = perf_counter()

    pixels.show()
    sleep(wait_ms / 1000.0)
    # end = perf_counter()
    # print(f"show() took: {end-start}s")


    # sleep(wait_ms / 1000.0)
    for i in range(0, pixels.n, 3):
        pixels[order_to_array(i + counter_b)] = (0, 0, 0)
    pixels.show()
