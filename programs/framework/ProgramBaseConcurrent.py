from threading import Thread
from typing import Callable

import pigpio

from controller.Light import Light
from controller.Servo180 import Servo180
from patterns.ServoPatternsConcurrent import ServoPatternsConcurrent
from programs.framework.ProgramBase import ProgramBase


class ProgramBaseConcurrent(ProgramBase):
    def __init__(self,
                 func1: Callable[[pigpio.pi, Servo180, Light, Callable[[float], None], ServoPatternsConcurrent], None],
                 func2: Callable[[pigpio.pi, Servo180, Light, Callable[[float], None], ServoPatternsConcurrent], None]):
        super().__init__()
        self.servo_patterns = ServoPatternsConcurrent(self.serv_laser, self.serv_base, self.wait_for_laser_to_get_to, self.wait_for_base_to_get_to)
        # self.laser_patterns = LightPatterns()

        self.t1 = Thread(target=lambda: func1(self.pi, self.serv_base, self.laser, self.wait_for_laser_to_get_to,
                                              self.servo_patterns))
        self.t2 = Thread(target=lambda: func2(self.pi, self.serv_laser, self.laser, self.wait_for_base_to_get_to,
                                              self.servo_patterns))

    def start(self):
        self.t1.start()
        self.t2.start()

    def wait_for_laser_to_get_to(self, degrees: float):
        print("LASER to... " + str(degrees))
        while not self.serv_laser.is_at_degree(degrees):
            pass
        print("\t\tTHERE")

    def wait_for_base_to_get_to(self, degrees: float):
        print("BASE to... " + str(degrees))
        while not self.serv_base.is_at_degree(degrees):
            pass
        print("\t\tTHERE")

    # override
    def end(self):
        print("Stopping...")
        self.t1.join()
        self.t2.join()
        print("Done.")
        super().end()
