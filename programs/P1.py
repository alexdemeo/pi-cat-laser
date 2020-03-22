import pigpio

from controller import Servo180, Light


def start(pi, down, up, laser):
    # type: (pigpio.pi, Servo180, Servo180, Light) -> None
    up.turn_to_degree2(40, 100)
    down.turn_to_degree2(90, 50)
