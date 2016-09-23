import rooms
import agent
from argument import *

rooms = rooms.load_rooms('locations.yaml')
teachers = agent.load_agents('teachers.yaml')

for teacher in teachers:
    print(teacher)
	
print('')

for room in rooms:
    print(room)

fw = ArgumentationFramework()


 

	
