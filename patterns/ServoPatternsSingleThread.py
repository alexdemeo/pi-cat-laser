# def base(pi, s, l, waitForDeg):
# def laser(pi, s, l, waitForDeg):
from time import sleep, time
from threading import Thread
from controller import Servo
from controller import Servo180


class ServoPatternsSingleThread:
    # base: positive = counterclockwise, negative = clockwise
    # laser: positive = up, negative = down
    def __init__(self, serv_base: Servo180, serv_laser: Servo180):
        self.serv_base = serv_base
        self.serv_laser = serv_laser


    def __current_millis(self):
        return int(round(time() * 1000))

    def center(self, interval_seconds):
        self.turn_servos_to(90, 90, interval_seconds)


    def diamond(self, w: int, h: int, interval_seconds: float):
        """
        :param interval_seconds:
        :param w: diamond width in degrees
        :param h: diamond height in degrees
        :param speed:
        """
        m1 = self.__current_millis()
        self.turn_servos_by(w / 2, h / 2, interval_seconds / 4)
        self.turn_servos_by(w / 2, -h / 2, interval_seconds / 4)
        self.turn_servos_by(-w / 2, -h / 2, interval_seconds / 4)
        self.turn_servos_by(-w / 2, h / 2, interval_seconds / 4)
        m2 = self.__current_millis()
        print("took " + str((m2 - m1) / 1000))

    def fan(self, degree_span_horizontal: float, degree_span_vertical: float,
            degree_vertical_step: float, interval_seconds: float):
        """
        Like the wifi symbol
        :param degree_span_horizontal: span clockwise to turn for each fan iteration
        :param degree_span_vertical: span vertically to fan upwards
        :param degree_vertical_step: the step to go up for each iteration. Must evenly divide degree_span_vertical
        :param interval_seconds:
        :return:
        """
        if not degree_span_vertical % degree_vertical_step == 0:
            raise ValueError("degree_span_vertical should be a multiple of degree_vertical_step")

        steps = int(degree_span_vertical / degree_vertical_step)
        for i in range(0, steps):
            self.turn_servos_by(degree_span_horizontal * (1 if i % 2 == 0 else -1),
                                -degree_vertical_step, interval_seconds / steps)

    def turn_servos_by(self, base_degrees: float, laser_degrees: float, interval_seconds: float):
        """
        :param base_degrees:
        :param laser_degrees:
        :param interval_seconds:
        :return:
        """
        base_degrees *= -1  # make the base go clockwise on positive
        laser_degrees *= -1  # make the laser go clockwise on positive
        base_current_degrees = self.serv_base.current_rotation()
        laser_current_degrees = self.serv_laser.current_rotation()
        to_base = Servo.sanitize_degree(base_current_degrees + base_degrees)
        to_laser = Servo.sanitize_degree(laser_current_degrees + laser_degrees)
        print("to_base=" + str(to_base) + ", to_laser=" + str(to_laser))
        self.turn_servos_to(to_base, to_laser, interval_seconds)

    def turn_servos_to(self, base_degrees: float, laser_degrees: float, interval_seconds: float):
        """
        :param base_degrees:
        :param laser_degrees:
        :param interval_seconds:
        :return:
        """
        if base_degrees < 0 or base_degrees > 180:
            raise ValueError(str(base_degrees) + " base_degrees should be between 0 and 180")
        if laser_degrees < 0 or laser_degrees > 180:
            raise ValueError(str(laser_degrees) + " laser_degrees should be between 0 and 180")

        base_current_degrees = self.serv_base.current_rotation()
        laser_current_degrees = self.serv_laser.current_rotation()
        niters_base = int(abs(base_current_degrees - base_degrees) / Servo.STEP_WIDTH)
        niters_laser = int(abs(laser_current_degrees - laser_degrees) / Servo.STEP_WIDTH)
        if not self.serv_base.is_at_degree(base_degrees):
            if niters_base == 0:
                print("at " + str(base_current_degrees) + " to " + str(base_degrees))
            delay_base = interval_seconds / niters_base
        else:
            delay_base = -1
        if not self.serv_laser.is_at_degree(laser_degrees):
            if niters_laser == 0:
                print("at " + str(laser_current_degrees) + " to " + str(laser_degrees))
            delay_laser = interval_seconds / niters_laser
        else:
            delay_laser = -1
        multiplier_base = 1 if base_degrees > base_current_degrees else -1
        multiplier_laser = 1 if laser_degrees > laser_current_degrees else -1

        def base():
            for i in range(0, niters_base):
                self.serv_base.turn_by_degree_immediate(Servo.STEP_WIDTH * multiplier_base)
                sleep(delay_base)
            print("BASE AT " + str(self.serv_base.current_rotation()))

        def laser():
            for i in range(0, niters_laser):
                self.serv_laser.turn_by_degree_immediate(Servo.STEP_WIDTH * multiplier_laser)
                sleep(delay_laser)
            print("LASER AT " + str(self.serv_laser.current_rotation()))

        t1 = Thread(target=base) if delay_base != -1 else None
        t2 = Thread(target=laser) if delay_laser != -1 else None
        if t1:
            t1.start()
        if t2:
            t2.start()

        if t1:
            t1.join()
        if t2:
            t2.join()
