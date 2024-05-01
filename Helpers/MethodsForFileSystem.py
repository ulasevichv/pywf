import re
from vendor.pywf.Helpers.Dict import Dict
from vendor.pywf.Helpers.MethodsForStrings import MethodsForStrings


class MethodsForFileSystem:
    @classmethod
    def readEnvFile(cls, filePath, conversionRules: Dict):
        f = open(filePath, 'r')
        content = f.read()
        f.close()

        variables = Dict()

        rawLines = content.split("\n")
        for i, line in enumerate(rawLines):
            line = line.strip()

            if line == '':
                continue

            if line[:1] == '#' or line[:1] == ';':
                continue

            parts = re.findall(r'^[ ]*(\w*)[ ]*=[ ]*(.*)$', line)

            if len(parts) != 1:
                raise Exception('Invalid .env-file structure at line ' + str(i))
            if len(parts[0]) != 2:
                raise Exception('Invalid .env-file structure at line ' + str(i))

            varName = str(parts[0][0])
            value = str(parts[0][1])

            if variables.get(varName) is not None:
                continue

            value = value.strip()

            # value.strip('"') is not used here, because it does not check that BOTH quotes are present
            if len(value) >= 2 and value[0:1] == '"' and value[-1:] == '"':
                value = value[1:-1]

            if str(value).lower() == 'none' or str(value) == 'null':
                value = None

            if conversionRules.get(varName) is not None:
                value = cls.convertValue(value, conversionRules.get(varName))

            variables[varName] = value

        return variables

    @classmethod
    def convertValue(cls, s: str, targetTypeName: str):
        match targetTypeName:
            case 'bool':
                return MethodsForStrings.strToBool(s)
            case _:
                return s
