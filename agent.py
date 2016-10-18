import yaml
from collections import defaultdict
from argument.sizeargument import SizeArgument
from argument.beamerargument import BeamerArgument
from argument.roompreferenceargument import RoomPreferenceArgument
from argument.argument import Counter
from argument.claim import Claim

class Agent(object):
    def __init__(self, name, courses = [], room_preferences = {}, occupied = []):
        self.name = name
        self.courses = courses
        self.active_course = None
        self.occupied = occupied
        self.room_preferences = room_preferences

    def __str__(self):
        return '#<{} | courses: {} | preferences: {}>'.format(self.name, str(self.courses), str(self.room_preferences))

    def get_name(self):
        return self.name

    def make_counter(self, fw, room):
        own_ungrounded = [arg for arg in fw.get_arguments()
                          if arg.owner == self
                          and not fw.is_grounded(arg)]


        own_grounded = [arg for arg in fw.get_grounded()
                          if arg.owner == self]


        if len(own_ungrounded) > 0:
            for arg in own_ungrounded:
                if isinstance(arg, Claim):
                    supports = fw.get_supports(arg)
                    if len(supports) < 3:
                        types = [type(arg) for arg,_ in supports]
                        if  (SizeArgument not in types):
                            size_arguments = [arg for arg in own_grounded
                                              if isinstance(arg, SizeArgument)]
                            if len(size_arguments) < 1:
                                return Counter("support",
                                    SizeArgument(fw, self, room, self.active_course.students), arg)
                            else:
                                return Counter("support", size_arguments[0], arg)
                        elif  (BeamerArgument not in types):
                            size_arguments = [arg for arg in own_grounded
                                              if isinstance(arg, BeamerArgument)]
                            if len(size_arguments) < 1:
                                return Counter("support",
                                    BeamerArgument(fw, self, room, self.active_course.beamer), arg)
                            else:
                                return Counter("support", size_arguments[0], arg)
                        elif  (RoomPreferenceArgument not in types):
                            size_arguments = [arg for arg in own_grounded
                                              if isinstance(arg, RoomPreferenceArgument)]
                            if len(size_arguments) < 1:
                                return Counter("support",
                                    RoomPreferenceArgument(fw, self, room), arg)
                            else:
                                return Counter("support", size_arguments[0], arg)

        grounded_others = [arg for arg in fw.get_supports(grounded = True)
                            if arg[1].owner != self]
        if len(grounded_others) != 0:
            for arg in grounded_others:
                if not fw.is_undercut(*arg):
                    att = self.construct_attack(fw, room, arg)
                    if att:
                        return att
        else:
            for arg in own_ungrounded:
                for att in fw.get_attacks(argument = arg):
                    if not isinstance(att[0], Claim):
                        counter = self.construct_attack(fw,room, att)
                        if counter:
                            return counter
        return None

    #Make an argument. Agent will first try to make a size argument. If it can't, it'll try a beamer argument. If it also can't do that, it will always make a preference argument.
    def construct_attack(self, fw, room, arg):
        own_arguments = [arg for arg in fw.get_arguments()
                            if arg.owner == self]
        other = arg[0].owner.active_course

        #Size argument
        if self.active_course.students >= other.students and isinstance(arg[0], SizeArgument):
            list_size_arguments = [a for a in own_arguments
                        if isinstance(a, SizeArgument)]
            if len(list_size_arguments) != 0:

                if fw.is_grounded(list_size_arguments[0]):
                    return Counter("undercut", list_size_arguments[0], arg)
            else:
                return Counter("undercut",
                        SizeArgument(fw, self, room, self.active_course.students),
                        arg)

        #Beamer argument
        elif self.active_course.beamer >= other.beamer and isinstance(arg[0], BeamerArgument):
            list_beamer_arguments = [a for a in own_arguments
                        if isinstance(a, BeamerArgument)]
            if len(list_beamer_arguments) != 0:
                if fw.is_grounded(list_beamer_arguments[0]):
                    return Counter("undercut", list_beamer_arguments[0], arg)
            else:
                return Counter("undercut",
                        BeamerArgument(fw, self, room, self.active_course.beamer),
                        arg)

        #Preference argument
        elif isinstance(arg[0], RoomPreferenceArgument) and \
                self.room_preferences[room.name] >= arg[0].owner.room_preferences[room.name]:
            list_preference_arguments = [a for a in own_arguments
                        if isinstance(a, RoomPreferenceArgument)]
            if len(list_preference_arguments) != 0:
                if fw.is_grounded(list_preference_arguments[0]):
                    return Counter("undercut", list_preference_arguments[0], arg)
            else:
                return Counter("undercut",
                        RoomPreferenceArgument(fw, self, room),
                        arg)

        return None

    def has_won(self, room):
        slot = (room.day, room.start_time, room.end_time)
        self.occupied.append(slot)
        self.active_course.lectures -= 1
        return self.active_course

    def is_free(self, day, start, end):
        for d, s, e in self.occupied:
            if d != day:
                continue
            if start < s < end or start < e < end or \
                (s < start and e > end):
                return False
        return (day, start, end) not in self.occupied

class Course:
    def __init__(self, name, size, lectures, beamer):
        self.name = name
        self.students = size
        self.lectures = lectures
        self.beamer = beamer

    def __str__(self):
        return '#<{} | size: {} | lectures {} | beamer {} >'.format(self.name, self.students, self.lectures, self.beamer)

class Room_Preference:
    def __init__(self, room, weight):
        self.room = room
        self.weight = weight

    def __str__(self):
        return '#< room {} | weight {} >'.format(self.room, self.weight)

def load_agents(filename):
    with open(filename, 'r') as f:
        agent_doc = yaml.load(f)

    teacher_list = []
    for teacher in agent_doc['teachers']:
        prefDict = defaultdict(lambda:0.5)
        for preference in teacher['preferences']:
            prefDict[preference['room']] = float(preference['weight'])

        r = Agent(teacher['name'],
            [Course(course['name'], course['students'], course['lectures'], course['beamer'])
                for course in teacher['courses']],
            prefDict)
        teacher_list.append(r)
    return teacher_list
