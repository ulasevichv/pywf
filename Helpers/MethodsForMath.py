class MethodsForMath:
    @classmethod
    def isNumeric(cls, value):
        if isinstance(value, (int, float, complex)):
            return True

        try:
            int(value)
            return True
        except ValueError:
            pass

        try:
            float(value)
            return True
        except ValueError:
            pass

        try:
            complex(value)
            return True
        except ValueError:
            pass

        return False

    @classmethod
    def toNumeric(cls, value):
        if isinstance(value, (int, float, complex)):
            return value

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        try:
            return complex(value)
        except ValueError:
            pass

        raise ValueError('Value cannot be converted to any numeric type')
