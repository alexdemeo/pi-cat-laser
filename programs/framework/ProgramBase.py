import abc
import os

import pigpio

from controller.Light import Light
from controller.Servo180 import Servo180

SERVO_1_PIN = 12  # GPIO: 12, PIN: 32
SERVO_2_PIN = 13  # GPIO: 13, PIN: 33
LASER_PIN = 4
FAN_PIN = 21


class ProgramBase(abc.ABC):
    def __init__(self):
        self.pi = pigpio.pi()
        self.pi.write(FAN_PIN, pigpio.LOW)
        self.serv_base = Servo180(self.pi, SERVO_1_PIN)
        self.serv_laser = Servo180(self.pi, SERVO_2_PIN)
        self.laser = Light(self.pi, LASER_PIN)

    @abc.abstractmethod
    def start(self):
        pass

    def end(self):
        self.laser.off()
        self.serv_base.reset()
        self.serv_laser.reset()
        self.pi.write(FAN_PIN, pigpio.LOW)
        self.pi.stop()
