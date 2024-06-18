from subprocess import Popen
from time import sleep

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Language.Lang import Lang


class MultiProcessing:
    @classmethod
    def getProcessLaunchResult(cls, processHandle: Popen) -> Dict:
        sleep(0.1)  # Required so that newly started process had time to write to PID-file.

        # for line in processHandle.stdout:
        #     print(line, end='')

        # timePassed = 0
        # timeout = 1
        # sleepInterval = 0.05
        # while processHandle.poll() is None and timePassed < timeout:
        #     line = processHandle.stdout.readline()
        #     print(line, end='')
        #
        #     sleep(sleepInterval)
        #     timePassed += sleepInterval

        # line = processHandle.stdout.readline()
        # print(line, end='')

        return Dict({
            'success': False,
            'error': Lang.msg('PROCESS.LAUNCH_ERROR.TIMEOUT')
        })
