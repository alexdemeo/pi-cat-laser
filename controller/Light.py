import pigpio


class Light:
    def __init__(self, pi, gpio_pin):
        self.pi = pi  # type: pigpio.pi
        self.pin = gpio_pin

    def turn_on(self):
        self.pi.write(self.pin, pigpio.HIGH)

    def turn_off(self):
        self.pi.write(self.pin, pigpio.LOW)
