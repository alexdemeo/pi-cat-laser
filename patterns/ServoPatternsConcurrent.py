# def base(pi, s, l, waitForDeg):
# def laser(pi, s, l, waitForDeg):
import threading
from threading import Thread
from typing import Callable

from controller import Servo180


class ServoPatternsConcurrent:
    def __init__(self, serv_base: Servo180, serv_laser: Servo180,
                 wait_for_base_to_get_to: Callable[[float], None],
                 wait_for_laser_to_get_to: Callable[[float], None]):
        self.serv_base = serv_base  # type: Servo180
        self.serv_laser = serv_laser
        self.wait_for_base_to_get_to = wait_for_base_to_get_to
        self.wait_for_laser_to_get_to = wait_for_laser_to_get_to

    def __run_pattern(self, base, laser):
        t1 = Thread(target=base)
        t2 = Thread(target=laser)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def center(self):
        self.__run_pattern(self.serv_base.reset, self.serv_laser.reset)

    def wait_for_base_to_turn_by(self, degrees: float):
        self.wait_for_base_to_get_to(self.serv_base.current_rotation() + degrees)

    def wait_for_laser_to_turn_by(self, degrees: float):
        self.wait_for_laser_to_get_to(self.serv_laser.current_rotation() + degrees)

    def diamond(self, w: int, h: int, speed: int):
        """
        :param w: diamond width in degrees
        :param h: diamond height in degrees
        :param speed:
        """

        def base():
            self.serv_base.turn_by_degree(w / 2, speed)
            self.wait_for_laser_to_turn_by(h / 2)
            self.serv_base.turn_by_degree(w / 2, speed)
            self.wait_for_laser_to_turn_by(-h / 2)
            self.serv_base.turn_by_degree(-w / 2, speed)
            self.wait_for_laser_to_turn_by(-h / 2)
            self.serv_base.turn_by_degree(-w / 2, speed)
            self.wait_for_laser_to_turn_by(h / 2)

        def laser():
            self.serv_laser.turn_by_degree(h / 2, speed)
            self.wait_for_base_to_turn_by(w / 2)
            self.serv_laser.turn_by_degree(-h / 2, speed)
            self.wait_for_base_to_turn_by(w / 2)
            self.serv_laser.turn_by_degree(-h / 2, speed)
            self.wait_for_base_to_turn_by(-w / 2)
            self.serv_laser.turn_by_degree(h / 2, speed)
            self.wait_for_base_to_turn_by(-w / 2)

        self.__run_pattern(base, laser)

    def pattern1(self):
        def base():
            s = self.serv_base
            waitForDeg = self.wait_for_laser_to_get_to

            s.turn_to_degree(90, 75)

        def laser():
            s = self.serv_laser
            waitForDeg = self.wait_for_base_to_get_to
            waitForDeg(45)
            s.turn_to_degree(45, 80)

        self.__run_pattern(base, laser)
