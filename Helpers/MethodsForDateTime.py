from datetime import datetime, timezone

from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings


class MethodsForDateTime:
    @classmethod
    def getCurrentTimestamp(cls) -> int:
        import math
        return math.floor(datetime.now(timezone.utc).timestamp())

    @classmethod
    def getCurrentTimestampMS(cls) -> float:
        return round(datetime.now(timezone.utc).timestamp(), 3)

    @classmethod
    def getCurrentTimestampMcS(cls) -> float:
        return datetime.now(timezone.utc).timestamp()

    @classmethod
    def getCurrentTimestampStr(cls) -> str:
        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def getCurrentTimestampStrMS(cls) -> str:
        dt = datetime.now(timezone.utc)
        milliseconds = round(dt.microsecond / 1000)
        dtStr = dt.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(milliseconds)
        return MethodsForStrings.alignString(dtStr, 23, 'left', '0')

    @classmethod
    def utcTimestampMSToStrMS(cls, timestamp: float | int):
        dt = datetime.fromtimestamp(timestamp / 1000, timezone.utc)
        milliseconds = round(dt.microsecond / 1000)
        dtStr = dt.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(milliseconds)
        return MethodsForStrings.alignString(dtStr, 23, 'left', '0')
