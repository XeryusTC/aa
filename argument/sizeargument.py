from argument import Argument
from argument.claim import Claim

class SizeArgument(Argument):
    def __init__(self, framework, size, room, name = None):
        super(SizeArgument, self).__init__(framework, name)
        self._size = size
        self._room = room

    def get_size(self):
        return self._size

    def get_room(self):
        return self._room

    def can_attack(self, other):
        if isinstance(other, SizeArgument):
            return self.get_room() == other.get_room() and \
                    self.get_size() >= other.get_size()
        elif isinstance(other, Claim):
            return self.get_room() == other.get_room()
        else:
            return False
