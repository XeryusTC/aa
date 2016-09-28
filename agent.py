import yaml
from argument.sizeargument import SizeArgument
from argument.argument import Counter

class Agent(object):
    def __init__(self, name, courses = []):
        self.name = name
        self.courses = courses
        self.active_course = None

    def __str__(self):
       return '#<{} | course: {} >'.format(self.name, self.courses)

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

    def construct_attack(self, fw, room, arg):
        own_arguments = [arg for arg in fw.get_arguments()
                            if arg.owner == self]
        other = arg.owner.active_course
        if self.active_course.students >= other.students:
            sizearg = [a for a in own_arguments
                        if isinstance(a, SizeArgument)]
            if len(sizearg) != 0:
                if fw.is_grounded(sizearg[0]):
                    return Counter("attack", sizearg[0], arg)
            else:
                return Counter("attack", 
                        SizeArgument(fw, self, room, self.active_course.students),
                        arg)
        return None

class Course:
    def __init__(self, name, size, lectures):
        self.name = name
        self.students = size
        self.lectures = lectures

    def __str__(self):
       return '#<{} | size: {} | lectures {} >'.format(self.name, self.students,
            self.lectures)

def load_agents(filename):
    with open(filename, 'r') as f:
        agent_doc = yaml.load(f)

    teacher_list = []
    for teacher in agent_doc['teachers']:
        r = Agent(teacher['name'],
            [Course(course['name'], course['students'], course['lectures'])
                for course in teacher['courses']])
        teacher_list.append(r)
    return teacher_list
