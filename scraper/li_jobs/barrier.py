import time
from collections import deque
from typing import Optional


class FrequencyBarrier:
    def __init__(self, rpm: Optional[int] = None, min_delay: float = 0.0):
        self.queue = deque()
        self.rpm = rpm
        self.min_delay = min_delay

    def wait(self):
        minute_ago = time.monotonic() - 60
        while self.queue and self.queue[0] < minute_ago:
            self.queue.popleft()

        delay = 0
        if self.rpm is not None and len(self.queue) >= self.rpm:
            delay = self.queue[0] + 60 - time.monotonic()
        if self.queue:
            delay = max(delay, self.queue[-1] + self.min_delay - time.monotonic())

        time.sleep(delay)
        self.queue.append(time.monotonic())
