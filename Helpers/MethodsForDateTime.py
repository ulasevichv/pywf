from datetime import (datetime, timezone)

from .MethodsForStrings import MethodsForStrings


class MethodsForDateTime:
    # ==================================================
    # Retrieving current UTC timestamp.
    # ==================================================

    @classmethod
    def getCurrentTimestamp(cls) -> int:
        from math import floor
        return floor(datetime.now(timezone.utc).timestamp())

    @classmethod
    def getCurrentTimestampStr(cls) -> str:
        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def getCurrentTimestampMilliSec(cls) -> float:
        return round(datetime.now(timezone.utc).timestamp(), 3)

    @classmethod
    def getCurrentTimestampMilliSecStr(cls) -> str:
        dt = datetime.now(timezone.utc)
        milliseconds = round(dt.microsecond / 1000)
        dtStr = dt.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(milliseconds)
        return MethodsForStrings.alignString(dtStr, 23, 'left', '0')

    @classmethod
    def getCurrentTimestampMicroSec(cls) -> float:
        return datetime.now(timezone.utc).timestamp()

    @classmethod
    def getCurrentTimestampMicroSecStr(cls) -> str:
        dt = datetime.now(timezone.utc)
        microsecond = dt.microsecond
        dtStr = dt.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(microsecond)
        return MethodsForStrings.alignString(dtStr, 26, 'left', '0')

    # ==================================================
    # Reformatting timestamps.
    # ==================================================

    # Converting UTC timestamp in milliseconds into a DateTime-string with milliseconds.
    @classmethod
    def utcTimestampMilliSecToStr(cls, timestamp: float | int) -> str:
        dt = datetime.fromtimestamp(timestamp / 1000, timezone.utc)
        milliseconds = round(dt.microsecond / 1000)
        dtStr = dt.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(milliseconds)
        return MethodsForStrings.alignString(dtStr, 23, 'left', '0')

    # ==================================================
    # General.
    # ==================================================

    @classmethod
    def numSecondsInIntervalAbs(cls, dt1: datetime, dt2: datetime) -> int:
        import math

        diffDT = dt2 - dt1
        return abs(math.floor(diffDT.total_seconds()))
