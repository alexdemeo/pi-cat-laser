import _thread
from threading import Thread

import pigpio

from controller.Light import Light
from controller.Servo180 import Servo180

SERVO_1_PIN = 13  # GPIO: 12, PIN: 32
SERVO_2_PIN = 12  # GPIO: 13, PIN: 33
LASER_PIN = 4


class ProgramBaseConcurrent:
    def __init__(self, func1, func2):
        self.pi = pigpio.pi()
        self.serv_base = Servo180(self.pi, SERVO_1_PIN)
        self.serv_laser = Servo180(self.pi, SERVO_2_PIN)
        self.laser = Light(self.pi, LASER_PIN)
        self.laser.turn_on()
        self.t1 = Thread(target=lambda: func1(self.pi, self.serv_base, self.laser, self.wait_for_laser_to_get_to))
        self.t2 = Thread(target=lambda: func2(self.pi, self.serv_laser, self.laser, self.wait_for_base_to_get_to))
        self.t1.start()
        self.t2.start()

    def wait_for_laser_to_get_to(self, degrees):
        while self.serv_laser.current_rotation() - degrees >= self.serv_laser.step_width:
            pass

    def wait_for_base_to_get_to(self, degrees):
        while self.serv_base.current_rotation() - degrees >= self.serv_base.step_width:
            pass

    def end(self):
        self.t1.join()
        self.t2.join()
        self.laser.turn_off()
        self.serv_base.reset()
        self.serv_laser.reset()
        self.pi.stop()
