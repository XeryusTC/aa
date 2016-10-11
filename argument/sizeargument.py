from argument import Argument
from argument.claim import Claim

class SizeArgument(Argument):
    def __init__(self, framework, owner, room, size, name = None):
        super(SizeArgument, self).__init__(framework, owner, name)
        self.room = room
        self.size = size #Requirement of the course

    def __repr__(self):
        return "#<size argument number: " + str(self.get_name()) + \
            " | owner: "+ str(self.owner.name) +" | available: "+ \
            str(self.room.size) +" required: "+str(self.size) +">"        
        
    def get_size(self):
        return self.size

    def get_room(self):
        return self.room

    def can_attack(self, other):
        if isinstance(other, SizeArgument):
            return self.get_room() == other.get_room() and \
                    self.get_size() >= other.get_size()
        elif isinstance(other, Claim):
            return self.get_room() == other.get_room()
        else:
            return False
