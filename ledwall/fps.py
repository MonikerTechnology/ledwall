import logging
import time

class FPS:
    """
    Usage:
    fps = FPS(30)
    while True:
        fps.maintain()
    """

    def __init__(self, target_fps, name='FPS'):
        self.logger = logging.getLogger(f'audio_processor.{name}')
        self.logger.info('creating an instance of FPS')
        self.one_sec = 0  # moves every second
        self.sleep_fps = .005  # Guess!
        self.loop_count = 0  # to track FPS
        self.start_time = time.time()
        self.target_fps = target_fps
        self.true_fps = target_fps
        self.elapsed = 0

    def maintain(self):
        self.elapsed = time.time() - self.start_time
        self.loop_count += 1
        if self.one_sec < self.elapsed:
            self.logger.debug(f"FPS: {self.true_fps} - sleep: {self.sleep_fps}")
            self.one_sec += 1
            self.true_fps = self.loop_count
            # print options.fps
            # print ("Loops per sec: %i") % loopCount

            if self.true_fps < self.target_fps - 2:
                self.sleep_fps *= .95
            elif self.true_fps > self.target_fps + 2:
                self.sleep_fps *= 1.05
            self.loop_count = 0
        time.sleep(self.sleep_fps)
