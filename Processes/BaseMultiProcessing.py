# from subprocess import Popen
from time import sleep

from ..Helpers.Dict import Dict
from ..Helpers.Log import Log
from ..Language.Lang import Lang
from ..Helpers.Redis import Redis


class BaseMultiProcessing:
    # @classmethod
    # def getProcessLaunchResult(cls, processHandle: Popen) -> Dict:
    #     sleep(0.1)  # Required so that newly started process had time to write to PID-file.
    #
    #     # for line in processHandle.stdout:
    #     #     print(line, end='')
    #
    #     # timePassed = 0
    #     # timeout = 1
    #     # sleepInterval = 0.05
    #     # while processHandle.poll() is None and timePassed < timeout:
    #     #     line = processHandle.stdout.readline()
    #     #     print(line, end='')
    #     #
    #     #     sleep(sleepInterval)
    #     #     timePassed += sleepInterval
    #
    #     # line = processHandle.stdout.readline()
    #     # print(line, end='')
    #
    #     return Dict({
    #         'success': False,
    #         'error': Lang.msg('PROCESS.LAUNCH_ERROR.TIMEOUT')
    #     })

    @classmethod
    def showProcessesLaunchResult(cls, redisStartupQueueNamePrefix: str, pids: list[int]) -> list[Dict]:
        sleep(len(pids) * 0.5)  # Required so that newly started process had time to write to PID-file.

        timeout = 1
        timePassed = 0
        sleepInterval = 0.2

        launchResults: list[Dict] = []
        for pid in pids:
            launchResults.append(Dict({
                'pid': pid,
                'msg': None
            }))
        respondedPIDs: list[int] = []

        while timePassed < timeout:
            if len(respondedPIDs) == len(pids):
                break

            for pid in pids:
                if pid in respondedPIDs:
                    continue

                msg = Redis.lpop(redisStartupQueueNamePrefix + str(pid))

                if msg is not None:
                    result = [res for res in launchResults if res.pid == pid][0]

                    result.msg = msg

                    respondedPIDs.append(pid)

            timePassed += sleepInterval

        return launchResults
