import time

from programs.programs.P4 import start
from programs.framework.ProgramBaseSingleThread import ProgramBaseSingleThread

if __name__ == '__main__':
    # base = ProgramBaseConcurrent(base, laser)
    base = ProgramBaseSingleThread(start)
    base.start()
    time.sleep(1)
    base.end()
