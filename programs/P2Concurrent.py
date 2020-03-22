import pigpio

from controller import Servo180, Light

def base(pi, s, l, waitForDeg):
    # type: (pigpio.pi, Servo180, Light) -> None
    waitForDeg(90)
    s.turn_to_degree2(25, 25)
    pass

def laser(pi, s, l, waitForDeg):
    # type: (pigpio.pi, Servo180, Light) -> None
    s.turn_to_degree2(90, 10)
    pass

