from redis import Redis as LibRedis

from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings

from App.Kernel import Kernel


class Redis:
    _connection: LibRedis = None
    _tokenKeyPrefix: str = None
    _tokenDuration: int = None
    _TOKEN_LENGTH: int = 16

    @classmethod
    def getConnection(cls) -> LibRedis:
        if cls._connection is None:
            app = Kernel.getApp()

            cls._connection = LibRedis(
                host=app.envFile.get('REDIS_HOST'),
                port=app.envFile.get('REDIS_PORT'),
                db=app.envFile.get('REDIS_DATABASE'),
                password=app.envFile.get('REDIS_PASSWORD'),
                decode_responses=True)
        return cls._connection

    @classmethod
    def close(cls) -> None:
        if cls._connection is None:
            return

        cls._connection.close()

    # ==================================================
    # Command wrappers.
    # ==================================================

    @classmethod
    def setVar(cls, name: str, value) -> None:
        rds = cls.getConnection()

        if not isinstance(value, str):
            value = str(value)

        rds.set(name, value)

    @classmethod
    def getVar(cls, name: str) -> str:
        rds = cls.getConnection()

        return rds.get(name)

    @classmethod
    def keys(cls, pattern: str) -> list:
        rds = cls.getConnection()

        return rds.keys(pattern)

    @classmethod
    def ttl(cls, name: str) -> int:
        rds = cls.getConnection()

        return rds.ttl(name)

    @classmethod
    def delete(cls, name: str):
        rds = cls.getConnection()

        return rds.delete(name)

    # ==================================================
    # Queues.
    # ==================================================

    @classmethod
    def llen(cls, name: str) -> int:
        rds = cls.getConnection()

        return rds.llen(name)

    @classmethod
    def lrange(cls, name: str, start: int, end: int) -> list:
        rds = cls.getConnection()

        return rds.lrange(name, start, end)

    @classmethod
    def rpush(cls, name: str, *values: str | int | float) -> int:
        rds = cls.getConnection()

        return rds.rpush(name, *values)

    # ==================================================
    # User authorization tokens.
    # ==================================================

    @classmethod
    def getAuthTokenKeyPrefix(cls) -> str:
        if cls._tokenKeyPrefix is None:
            cls._tokenKeyPrefix = Kernel.getApp().envFile.get('REDIS_PROJECT_PREFIX') + ':user_token:'
        return cls._tokenKeyPrefix

    @classmethod
    def _getAuthTokenDuration(cls) -> int:
        if cls._tokenDuration is None:
            cls._tokenDuration = int(Kernel.getApp().envFile.get('REDIS_USER_TOKEN_DURATION'))
        return cls._tokenDuration

    @classmethod
    def _generateAuthToken(cls) -> str:
        return MethodsForStrings.generateRandomString(cls._TOKEN_LENGTH, 'lower')

    @classmethod
    def generateAndAddAuthToken(cls, userId: int) -> str:
        rds = cls.getConnection()

        token = cls._generateAuthToken()
        key = cls.getAuthTokenKeyPrefix() + token

        rds.setex(key, cls._getAuthTokenDuration(), userId)

        return token

    @classmethod
    def authTokenToUserId(cls, token: str, prolongToken: bool = True) -> int | None:
        rds = cls.getConnection()

        key = cls.getAuthTokenKeyPrefix() + token

        userId = rds.get(key)

        if userId is not None and prolongToken:
            rds.expire(key, cls._getAuthTokenDuration())

        return None if userId is None else int(userId)

    @classmethod
    def getAllAuthTokensInfo(cls) -> list[Dict]:
        rds = cls.getConnection()

        allKeys = rds.keys(cls.getAuthTokenKeyPrefix() + '*')

        results = []
        for key in allKeys:
            userId = int(rds.get(key))
            expiresIn = int(rds.ttl(key))
            results.append(Dict({
                'key': key,
                'userId': userId,
                'expiresIn': expiresIn
            }))
        return results

    @classmethod
    def deleteAuthToken(cls, token: str) -> None:
        rds = cls.getConnection()

        key = cls.getAuthTokenKeyPrefix() + token

        rds.delete(key)

    @classmethod
    def deleteAllAuthTokens(cls) -> int:
        rds = cls.getConnection()

        allKeys = rds.keys(cls.getAuthTokenKeyPrefix() + '*')

        numTokensDeleted = 0

        for key in allKeys:
            rds.delete(key)
            numTokensDeleted += 1

        return numTokensDeleted
