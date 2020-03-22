from controller.Servo import Servo
import time

SLOW_SPEED = 50
FAST_SPEED = 70

CENTER = 1500


class Servo360(Servo):
    def __init__(self, pi, gpio_pin):
        super().__init__(pi, gpio_pin)

    def turn_n_degree_slowest(self, n, clockwise=True):
        dir = CENTER + SLOW_SPEED * (-1 if not clockwise else 1)
        print("Spin " + str(self.pin) + " at " + str(dir))
        self.pi.set_servo_pulsewidth(self.pin, dir)
        time.sleep(n / 100)
        self.pi.set_servo_pulsewidth(self.pin, CENTER)
