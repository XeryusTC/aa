import yaml
from collections import defaultdict
from argument.sizeargument import SizeArgument
from argument.beamerargument import BeamerArgument
from argument.roompreferenceargument import RoomPreferenceArgument
from argument.argument import Counter

class Agent(object):
    def __init__(self, name, courses = [], room_preferences = {}):
        self.name = name
        self.courses = courses
        self.active_course = None
        self.room_preferences = room_preferences

    def __str__(self):
        return '#<{} | courses: {} | preferences: {}>'.format(self.name, self.courses, self.room_preferences)

    def get_name(self):
        return self.name
    
    def make_counter(self, fw, room):
        grounded_others = [arg for arg in fw.get_grounded()
                            if arg.owner != self]
        if len(grounded_others) != 0:
            for arg in grounded_others:
                att = self.construct_attack(fw, room, arg)
                if att:
                    return att
        else:
            own_ungrounded = [arg for arg in fw.get_arguments()
                                if arg.owner == self
                                if not fw.is_grounded(arg)]
            for arg in own_ungrounded:
                for att, _ in fw.get_attacks(argument = arg):
                    counter = self.construct_attack(fw,room, att)
                    if counter:
                        return counter
        return None

    #Make an argument. Agent will first try to make a size argument. If it can't, it'll try a beamer argument. If it also can't do that, it will always make a preference argument. 
    def construct_attack(self, fw, room, arg):
        own_arguments = [arg for arg in fw.get_arguments()
                            if arg.owner == self]
        other = arg.owner.active_course
        
        #Size argument
        if self.active_course.students >= other.students:
            list_size_arguments = [a for a in own_arguments
                        if isinstance(a, SizeArgument)]
            if len(list_size_arguments) != 0:
                if fw.is_grounded(list_size_arguments[0]):
                    return Counter("attack", list_size_arguments[0], arg)
            else:
                return Counter("attack", 
                        SizeArgument(fw, self, room, self.active_course.students),
                        arg)

        #Beamer argument    
        elif self.active_course.beamer >= other.beamer:
            list_beamer_arguments = [a for a in own_arguments
                        if isinstance(a, BeamerArgument)]
            if len(list_beamer_arguments) != 0:
                if fw.is_grounded(list_beamer_arguments[0]):
                    return Counter("attack", list_beamer_arguments[0], arg)
            else:
                return Counter("attack", 
                        BeamerArgument(fw, self, room, self.active_course.beamer),
                        arg)
            
        #Preference argument    
        else:
            list_preference_arguments = [a for a in own_arguments
                        if isinstance(a, RoomPreferenceArgument)]
            if len(list_preference_arguments) != 0:
                if fw.is_grounded(list_preference_arguments[0]):
                    return Counter("attack", list_preference_arguments[0], arg)
            else:
                return Counter("attack", 
                        RoomPreferenceArgument(fw, self, room),
                        arg)
            
        return None
    
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
