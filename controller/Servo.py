from abc import ABC

import pigpio


class Servo(ABC):
    def __init__(self, pi, gpio_pin):
        self.pi = pi  # type: pigpio.pi
        self.pi.set_PWM_frequency(gpio_pin, 50)
        self.pin = gpio_pin  # type: int
        self.pi.set_mode(gpio_pin, pigpio.ALT0)
        self.min = 500
        self.max = 2500

    def convert_from_degree(self, degree):
        if degree < 0 or degree > 180:
            raise ValueError(str(degree) + " should be between 0 and 180")
        return int(((self.max - self.min)/180) * degree + 500)

    def convert_to_degree(self, duty):
        if duty not in range(self.min, self.max + 1):
            raise ValueError(str(duty) + " should be between " + str(self.min) + " and " + str(self.max))
        return int((duty - 500) * (180 / (self.max - self.min)))
