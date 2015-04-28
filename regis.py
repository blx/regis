try:
    # py3k
    import winreg
except ImportError:
    # python 2
    try:
        import _winreg as winreg
    except ImportError:
        raise Exception("Congratulations, you're not using Windows. " +
                "This library has nothing to offer you. (Could not import " +
                "winreg module.)")

import itertools


class Regis(object):
    def __init__(self):
        self.reg = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                                    self.key)

    def get(self, key):
        val, typ = winreg.QueryValueEx(self.reg,
                                       key)
        return val

    def set(self, key, value):
        winreg.SetValueEx(self.reg,
                          key,
                          type=winreg.REG_SZ,
                          value=value)

    # can't call this DEL
    def delete(self, key):
        winreg.DeleteValue(self.reg,
                           key)

    def type(self, key):
        return self.get(key)[1] or None

    def exists(self, key):
        return key in self.keys()

    def keys(self):
        while True:
            yield self.items()[0]

    def items(self):
        try:
            for i in itertools.count(start=0):
                k, val, typ = winreg.EnumValue(self.reg,
                                               i)
                yield (k, val)
        except WindowsError:
            return
