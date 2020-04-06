from time import sleep

import pigpio

from controller import Servo180, Light
from patterns.ServoPatternsSingleThread import ServoPatternsSingleThread


BASE_BOTTOM = 98

P1 = (140, 80)
P2 = (140, 107)
P3 = (125, 95)
P4 = (120, 115)
P5 = (90, 95)
P6 = (90, 115)
P7 = (40, 95)
P8 = (40, 115)
P9 = (128, 50)
P10 = (130, 43)


def start(pi: pigpio.pi, down: Servo180, up: Servo180, laser: Light, sp: ServoPatternsSingleThread):
    # sp.turn_servos_by(-45, 0, 3)
    print("start()")
    # sp.turn_servos_to(130, 70, 2)
    laser.on()
    for i in range(0, 10):
        sp.turn_servos_to(*P6, 2)
        sp.turn_servos_to(*P4, 2)
        sp.turn_servos_to(*P2, 2)
        sp.turn_servos_to(*P1, 2)
        sp.turn_servos_to(*P3, 2)
        sp.fan(10, 30, 10, 5)
        sp.turn_servos_to(*P9, 2)
        sp.turn_servos_to(*P10, 2)
        sp.turn_servos_to(125, 95, 2)
        sp.turn_servos_to(*P5, 2)
        sp.fan(30, 15, 5, 5)
        sp.turn_servos_to(*P7, 4)
        sp.fan(25, 15, 5, 15)
        sp.turn_servos_to(*P8, 2)
