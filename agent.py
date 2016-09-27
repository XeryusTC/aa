import yaml
class Agent(object):
    def __init__(self, name, courses = []):
        self._name = name
        self._courses = courses

    def __str__(self):
       return '#<{} | course: {} >'.format(self._name, self._courses)

    def get_name(self):
        return self._name

    def make_counter(self, fw):
        return None

    def get_courses(self):
        return self._courses

class Course:
    def __init__(self, name, size):
        self._name = name
        self._size = size
        self._lectures = lectures

    def __str__(self):
       return '#<{} | size: {} | lectures {} >'.format(self._name, self._size, self._lectures)

        
    def get_lectures(self):
        return self._lectures
        
    def get_size(self):
        return self._size
    
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
