import pigpio


class Light:
    def __init__(self, pi, gpio_pin):
        self.pi = pi  # type: pigpio.pi
        self.pin = gpio_pin

    def on(self):
        self.pi.write(self.pin, pigpio.HIGH)

    def off(self):
        self.pi.write(self.pin, pigpio.LOW)
