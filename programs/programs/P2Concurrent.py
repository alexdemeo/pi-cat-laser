from typing import Callable

import pigpio

from controller import Servo180, Light
from patterns import ServoPatternsConcurrent
from time import sleep

def base(pi: pigpio.pi, s : Servo180, l: Light, waitForDeg: Callable[[float], None], servo_patterns: ServoPatternsConcurrent):
    servo_patterns.diamond(25, 50, 20)
    pass

def laser(pi: pigpio.pi, s : Servo180, l: Light, waitForDeg: Callable[[float], None], servo_patterns: ServoPatternsConcurrent):
    pass

