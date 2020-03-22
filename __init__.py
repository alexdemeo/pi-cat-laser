import time

from programs.P2Concurrent import base, laser
from programs.framework.ProgramBaseConcurrent import ProgramBaseConcurrent

if __name__ == '__main__':
    base = ProgramBaseConcurrent(base, laser)
    time.sleep(1)
    base.end()
