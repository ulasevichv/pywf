from App.Kernel import Kernel
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.Log import Log
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings


class Redis:
    _connection = None
    _tokenKeyPrefix: str = None
    _tokenDuration: int = None
    _TOKEN_LENGTH: int = 16

    @classmethod
    def getConnection(cls):
        if cls._connection is None:
            import redis

            app = Kernel.getApp()

            cls._connection = redis.Redis(
                host=app.envFile.get('REDIS_HOST'),
                port=app.envFile.get('REDIS_PORT'),
                db=app.envFile.get('REDIS_DATABASE'),
                password=app.envFile.get('REDIS_PASSWORD'),
                decode_responses=True)
        return cls._connection

    @classmethod
    def setVar(cls, name: str, value):
        rds = cls.getConnection()

        if not isinstance(value, str):
            value = str(value)

        rds.set(name, value)

    @classmethod
    def getVar(cls, name: str):
        rds = cls.getConnection()

        return rds.get(name)

    @classmethod
    def _getTokenKeyPrefix(cls):
        if cls._tokenKeyPrefix is None:
            cls._tokenKeyPrefix = Kernel.getApp().envFile.get('REDIS_USER_TOKEN_PREFIX') + ':token:'
        return cls._tokenKeyPrefix

    @classmethod
    def _getTokenDuration(cls):
        if cls._tokenDuration is None:
            cls._tokenDuration = int(Kernel.getApp().envFile.get('REDIS_USER_TOKEN_DURATION'))
        return cls._tokenDuration

    @classmethod
    def _generateAuthToken(cls):
        return MethodsForStrings.generateRandomString(cls._TOKEN_LENGTH, 'lower')

    @classmethod
    def generateAndAddAuthToken(cls, userId: int):
        rds = cls.getConnection()

        token = cls._generateAuthToken()
        key = cls._getTokenKeyPrefix() + token

        rds.setex(key, cls._getTokenDuration(), userId)

        return token

    @classmethod
    def authTokenToUserId(cls, token: str, prolongToken: bool = True):
        rds = cls.getConnection()

        key = cls._getTokenKeyPrefix() + token

        userId = rds.get(key)

        if userId is not None and prolongToken:
            rds.expire(key, cls._getTokenDuration())

        return None if userId is None else int(userId)

    @classmethod
    def getAllAuthTokensInfo(cls):
        rds = cls.getConnection()

        allKeys = rds.keys(cls._getTokenKeyPrefix() + '*')

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
    def deleteAuthToken(cls, token: str):
        rds = cls.getConnection()

        key = cls._getTokenKeyPrefix() + token

        rds.delete(key)

    @classmethod
    def deleteAllAuthTokens(cls):
        rds = cls.getConnection()

        allKeys = rds.keys(cls._getTokenKeyPrefix() + '*')

        numTokensDeleted = 0

        for key in allKeys:
            rds.delete(key)
            numTokensDeleted += 1

        return numTokensDeleted
