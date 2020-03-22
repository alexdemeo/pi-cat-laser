import pigpio

from controller.Light import Light
from controller.Servo180 import Servo180

SERVO_1_PIN = 13  # GPIO: 12, PIN: 32
SERVO_2_PIN = 12  # GPIO: 13, PIN: 33
LASER_PIN = 4


class ProgramBase:
    def __init__(self, func):
        self.pi = pigpio.pi()
        self.serv_base = Servo180(self.pi, SERVO_1_PIN)
        self.serv_laser = Servo180(self.pi, SERVO_2_PIN)
        self.laser = Light(self.pi, LASER_PIN)
        self.laser.turn_on()
        func(self.pi, self.serv_base, self.serv_laser, self.laser)

    def end(self):
        self.laser.turn_off()
        self.serv_base.reset()
        self.serv_laser.reset()
        self.pi.stop()
