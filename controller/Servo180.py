import time

import pigpio

from controller import Servo
from controller.Servo import STEP_WIDTH

DEBUG = True


class Servo180(Servo.Servo):
    def __init__(self, pi: pigpio.pi, gpio_pin: int):
        super().__init__(pi, gpio_pin)
        self.current_pulsewidth = Servo.MID
        self.step_pulsewidth = Servo.convert_from_degree(STEP_WIDTH) - Servo.MIN

    def current_rotation(self):
        """
        :return: The current angle in degrees of the servo
        """
        return Servo.convert_to_degree(self.current_pulsewidth)

    def shutoff(self):
        self.pi.set_servo_pulsewidth(self.pin, 0)

    def reset(self):
        self.turn_to_degree_inverted(90, 75)
        time.sleep(0.5)
        self.pi.set_servo_pulsewidth(self.pin, 0)

    def turn_to_degree(self, degree: float, speed: int):
        self.turn_to_degree_inverted(180 - degree, speed)

    def turn_by_degree(self, degree, speed):
        deg = Servo.sanitize_degree(self.current_rotation() + degree)
        self.log("turn_by_degree(" + str(degree)
                 + ", " + str(speed) + ") from "
                 + str(self.current_rotation()) + " to " + str(deg))
        self.turn_to_degree_inverted(deg, speed)

    def turn_to_degree_inverted(self, degree: float, speed: int):
        """
        speed: 1-100
        :param degree:
        :param speed:
        :return:
        """
        degree_pulsewidth = Servo.convert_from_degree(degree)
        sleep = (-(1 / 100) * speed + 1.1) * Servo.SPEED_SCALE
        counting_clockwise = degree_pulsewidth > self.current_pulsewidth
        self.log("turn_to_degree_inverted(" + str(degree) + ", " + str(speed) + ")")
        while True:
            self.pi.set_servo_pulsewidth(self.pin, self.current_pulsewidth)
            self.current_pulsewidth += self.step_pulsewidth * (1 if counting_clockwise else -1)
            time.sleep(sleep)
            if abs(self.current_pulsewidth - degree_pulsewidth) <= self.step_pulsewidth:
                self.current_pulsewidth = degree_pulsewidth
                self.pi.set_servo_pulsewidth(self.pin, self.current_pulsewidth)
                time.sleep(sleep)
                break

    def turn_to_degree_immediate(self, degree: float):
        duty = Servo.convert_from_degree(Servo.sanitize_degree(degree))
        self.current_pulsewidth = duty
        self.pi.set_servo_pulsewidth(self.pin, duty)

    def turn_by_degree_immediate(self, degree: float):
        duty = (Servo.convert_from_degree(Servo.sanitize_degree(abs(degree))) - Servo.MIN) * (-1 if degree < 0 else 1)

        self.log(str(duty) + " turn_by_degree_immediate(" + str(degree) + "), " +
                 str(self.current_rotation()) + " -> " + str(self.current_rotation() + degree) + " == " +
                 str(self.current_pulsewidth) + " -> " + str(self.current_pulsewidth + duty))
        self.current_pulsewidth += duty
        self.pi.set_servo_pulsewidth(self.pin, self.current_pulsewidth)

    def is_at_degree(self, degree: float):
        return Servo.is_degrees_equal(self.current_rotation(), degree)

    def log(self, s):
        if DEBUG:
            print(("base" if self.pin == 12 else "laser") + " -> " + s)
