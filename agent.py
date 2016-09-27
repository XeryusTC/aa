import yaml
class Agent(object):
    def __init__(self, name, courses = []):
        self.name = name
        self.courses = courses

    def __str__(self):
       return '#<{} | course: {} >'.format(self.name, self.courses)

    def make_counter(self, fw):
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
