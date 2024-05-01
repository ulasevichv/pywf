class MethodsForDateTime:
    @classmethod
    def getCurrentTimestampStr(cls):
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
