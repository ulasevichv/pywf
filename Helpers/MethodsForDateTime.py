from datetime import datetime, timezone


class MethodsForDateTime:
    @classmethod
    def getCurrentTimestamp(cls) -> int:
        import math
        return math.floor(datetime.now(timezone.utc).timestamp())

    @classmethod
    def getCurrentTimestampMS(cls) -> float:
        return round(datetime.now(timezone.utc).timestamp(), 3)

    @classmethod
    def getCurrentTimestampMCS(cls) -> float:
        return datetime.now(timezone.utc).timestamp()

    @classmethod
    def getCurrentTimestampStr(cls) -> str:
        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def getCurrentTimestampStrMS(cls) -> str:
        dt = datetime.now(timezone.utc)
        milliseconds = round(dt.microsecond / 1000)
        return dt.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(milliseconds)

    @classmethod
    def utcTimestampToStr(cls, timestamp: float | int):
        dt = datetime.fromtimestamp(timestamp / 1000, timezone.utc)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def utcTimestampToStrMS(cls, timestamp: float | int):
        dt = datetime.fromtimestamp(timestamp / 1000, timezone.utc)
        milliseconds = round(dt.microsecond / 1000)
        return dt.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(milliseconds)
