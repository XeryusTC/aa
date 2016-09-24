import yaml
class Agent(object):
    def __init__(self, name, course, students):
        self.name = name
        self.course = course
        self.students = students

    def __str__(self):
       return '{} | course: {} | students:{}'.format(self._name, self.course, self.students)
    
    def get_name(self):
        return self.name
		
    def get_course(self):
        return self.course
		
    def get_students(self):
        return self.students

def load_agents(filename):
    with open(filename, 'r') as f:
	    agent_doc = yaml.load(f)
		
    teacher_list = []

    for teacher in agent_doc['teachers']:
        r = Agent(teacher['name'], teacher['course'], teacher['students'])
        teacher_list.append(r)
    return teacher_list