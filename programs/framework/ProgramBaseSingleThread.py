from patterns.ServoPatternsSingleThread import ServoPatternsSingleThread
from programs.framework.ProgramBase import ProgramBase


class ProgramBaseSingleThread(ProgramBase):
    def __init__(self, func):
        super().__init__()
        self.servo_patterns = ServoPatternsSingleThread(self.serv_base, self.serv_laser)
        self.func = func

    def start(self):
        self.func(self.pi, self.serv_base, self.serv_laser, self.laser, self.servo_patterns)

