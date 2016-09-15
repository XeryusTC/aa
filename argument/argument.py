class Argument(object):
    def __init__(self):
        self._name = None

    def get_name(self):
        return self._name

    def set_name(self, name):
        if self._name is not None:
            raise RenameError("You can't rename an argument")
        else:
            self._name = name
        return self._name

    def can_attack(self, other):
        raise NotImplementedError("Implement `can_attack` yourself!")

    def can_undercut(self, other):
        raise NotImplementedError("Implement `can_undercut` yourself!")

    def can_support(self, other):
        raise NotImplementedError("Implement `can_support` yourself!")

class RenameError(Exception):
    pass
