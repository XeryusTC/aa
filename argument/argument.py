class Argument(object):
    def __init__(self, framework, owner, name = None):
        self.name = name
        self.fw = framework
        self.owner = owner
        self.fw.add_argument(self)

    def __repr__(self):
        try:
            return "#<argument name: " + str(self.get_name()) + \
                " | owner: "+ str(self.owner.name) +">"
        except: 
            return "#<argument name: " + str(self.get_name()) + \
                " | owner: "+ str(self.owner) +">"

    def get_name(self):
        return self.name

    def set_name(self, name):
        if self.name is not None:
            raise RenameError("You can't rename an argument")
        else:
            self.name = name
        return self.name

    def get_attacks(self, grounded = False):
        return self.fw.get_attacks(argument = self, grounded = grounded)

    def is_grounded(self):
        return self.fw.is_grounded(self)

    def can_attack(self, other):
        raise NotImplementedError("Implement `can_attack` yourself!")

    def can_undercut(self, other):
        raise NotImplementedError("Implement `can_undercut` yourself!")

    def can_support(self, other):
        raise NotImplementedError("Implement `can_support` yourself!")

class Counter(object):
    def __init__(self, type, attacker, attackee):
        self.type = type
        self.attacker = attacker
        self.attackee = attackee

    def __str__(self):
        return "#<counter type: " + self.type + \
                " | attacker: " + str(self.attacker) + \
                " | attackee: " + str(self.attackee) + ">"

class RenameError(Exception):
    pass
