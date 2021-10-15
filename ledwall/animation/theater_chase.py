from ledwall.color_utils import order_to_array, wheel
from time import sleep, perf_counter


def theaterChaseRainbow(pixels, counter, wait_ms=5):
    """Rainbow movie theater light style chaser animation."""
    start = perf_counter()
    for q in range(3):
        for i in range(0, pixels.n, 3):
            pixels[order_to_array(i + q)] = wheel((i + counter) % 255)
        pixels.show()
        # sleep(wait_ms / 1000.0)
        # for i in range(0, pixels.n, 3):
        #     pixels[order_to_array(i + q)] = (0, 0, 0)
        #     pixels.show()