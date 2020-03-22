import time

from controller.Servo import Servo


class Servo180(Servo):
    step_width = 2.5
    speed_scale = 1 / 10

    def __init__(self, pi, gpio_pin):
        super().__init__(pi, gpio_pin)
        self.current_pulsewidth = self.min
        self.step_pulsewidth = self.convert_from_degree(self.step_width) - 500
        self.reset()

    def __del__(self):
        try:
            self.reset()
        except AttributeError:
            pass

    def current_rotation(self):
        return self.convert_to_degree(self.current_pulsewidth)

    def reset(self):
        self.turn_to_degree(0, 75)

    def turn_to_degree2(self, degree, speed):
        self.turn_to_degree(180 - degree, speed)

    def turn_to_degree(self, degree, speed):
        """
        speed: 1-100
        :param degree:
        :param speed:
        :return:
        """
        degree_pulsewidth = self.convert_from_degree(degree)
        sleep = (-(1 / 100) * speed + 1.1) * self.speed_scale
        counting_clockwise = degree_pulsewidth > self.current_pulsewidth
        while True:
            self.pi.set_servo_pulsewidth(self.pin, self.current_pulsewidth)
            self.current_pulsewidth += self.step_pulsewidth * (1 if counting_clockwise else -1)
            time.sleep(sleep)
            if int(abs(self.current_pulsewidth - degree_pulsewidth)) <= self.step_pulsewidth:
                self.current_pulsewidth = degree_pulsewidth
                self.pi.set_servo_pulsewidth(self.pin, self.current_pulsewidth)
                time.sleep(sleep)
                break
