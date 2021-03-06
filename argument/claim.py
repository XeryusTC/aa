from argument import Argument

class Claim(Argument):
    def __init__(self, framework, agent, room, time, name = None):
        super(Claim, self).__init__(framework, agent, name)
        self._room = room
        self._time = time
        
    def __str__(self):
        return "#<claim name: " + str(self.get_name()) + " | owner: " + str(self.owner.name) + \
                " | room : " + str(self._room) + " | time: " + str(self._time) + ">"

    def get_room(self):
        return self._room

    def get_time(self):
        return self._time
    
    def can_attack(self, other):
        return (isinstance(other, Claim) and 
                self.get_room() == other.get_room() and
                self.get_time() == other.get_time())

    def can_undercut(self, other):
        return False

    def can_support(self, other):
        return False
