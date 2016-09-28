class Argument(object):
    def __init__(self, framework, owner, name = None):
        self._name = name
        self._fw = framework
        self.owner = owner
        self._fw.add_argument(self)

    def __repr__(self):
        return "#<argument name: " + str(self.get_name()) + ">"

    def get_name(self):
        return self._name

    def set_name(self, name):
        if self._name is not None:
            raise RenameError("You can't rename an argument")
        else:
            self._name = name
        return self._name

    def get_attacks(self, grounded = False):
        return self._fw.get_attacks(argument = self, grounded = grounded)

    def is_grounded(self):
        return self._fw.is_grounded(self)

    def can_attack(self, other):
        raise NotImplementedError("Implement `can_attack` yourself!")

    def can_undercut(self, other):
        raise NotImplementedError("Implement `can_undercut` yourself!")

    def can_support(self, other):
        raise NotImplementedError("Implement `can_support` yourself!")

class RenameError(Exception):
    pass
