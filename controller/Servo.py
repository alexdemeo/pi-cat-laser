from abc import ABC

import pigpio

STEP_WIDTH = 1  # degrees
SPEED_SCALE = 1 / 10
MIN = 500
MAX = 2500
MID = (MIN + MAX) / 2
TOLERANCE = 2  # degrees


def convert_from_degree(degree: float):
    if degree < 0 or degree > 180:
        raise ValueError(str(degree) + " should be between 0 and 180")
    return int(((MAX - MIN) / 180) * degree + MIN)


def convert_to_degree(duty: int):
    if duty not in range(MIN, MAX + 1):
        raise ValueError(str(duty) + " should be between " + str(MIN) + " and " + str(MAX))
    return (duty - MIN) * (180 / (MAX - MIN))


def sanitize_degree(degree: float):
    return 0 if degree < 0 else 180 if degree > 180 else degree


def sanitize_duty(duty: int):
    return MIN if duty < MIN else MAX if duty > MAX else duty


# Horrible grammar
def is_degrees_equal(deg1: float, deg2: float):
    return abs(deg1 - deg2) <= STEP_WIDTH


class Servo(ABC):
    def __init__(self, pi: pigpio.pi, gpio_pin: int):
        self.pi = pi  # type: pigpio.pi
        self.pi.set_PWM_frequency(gpio_pin, 50)
        self.pin = gpio_pin  # type: int
        self.pi.set_mode(gpio_pin, pigpio.ALT0)
