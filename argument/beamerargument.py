from argument import Argument
from argument.claim import Claim

class BeamerArgument(Argument):
    def __init__(self, framework, owner, room, beamer, name = None):
        super(BeamerArgument, self).__init__(framework, owner, name)
        self.room = room
        self.beamer = beamer #Requirement of the course

    def __repr__(self):
        return "#<argument number: " + str(self.get_name()) + \
            " | owner: "+ str(self.owner.name) +" | type: beamer argument | avail: "+ str(self.room.beamer) +" req: "+str(self.beamer) +">"
        
    def get_beamer(self):
        return self.beamer

    def get_room(self):
        return self.room

    def can_attack(self, other):
        if isinstance(other, BeamerArgument):
            return self.get_room() == other.get_room() and \
                    self.get_beamer() >= other.get_beamer()
        elif isinstance(other, Claim):
            return self.get_room() == other.get_room()
        else:
            return False
