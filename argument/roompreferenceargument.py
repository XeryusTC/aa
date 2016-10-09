from argument import Argument
from argument.claim import Claim

class RoomPreferenceArgument(Argument):
    def __init__(self, framework, owner, room, room_preference, name = None):
        super(RoomPreferenceArgument, self).__init__(framework, owner, name)
        self.room = room
        self.room_preference = room_preference

    def get_room_preference(self):
        return self.room_preference

    def get_room(self):
        return self.room

    def can_attack(self, other):
        if isinstance(other, RoomPreferenceArgument):
            return self.get_room() == other.get_room() and \
                    self.get_room_preference() >= other.get_room_preference()
        elif isinstance(other, Claim):
            return self.get_room() == other.get_room()
        else:
            return False
