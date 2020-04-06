import pigpio

from controller import Servo180, Light
from patterns.ServoPatternsSingleThread import ServoPatternsSingleThread


def start(pi: pigpio.pi, down: Servo180, up: Servo180, laser: Light, sp: ServoPatternsSingleThread):
        sp.turn_servos_by(-45, 15, 0.5)
        sp.fan(50, 20, 5, 5)
        sp.fan(50, -20, -5, 5)
        sp.turn_servos_by(0, -30, 2)
        sp.diamond(20, 40, 5)
        sp.center(4)
        sp.turn_servos_to(135, 90, 7)
        sp.turn_servos_to(45, 90, 4)
        sp.center(5)

