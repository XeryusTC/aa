import random

import rooms
import agent
from argument import *
from argument.claim import Claim
from argument.sizeargument import SizeArgument

class Support:
    def __init__(self):
        bullshit = []

def debateRoom(targetRoom, agents):
    interestedAgents = []
    claims = []
    fw = ArgumentationFramework()

    #Check if agent can make a claim, and if it can, make it.
    for agent in agents:
        if viableClaim(agent, targetRoom):
            interestedAgents.append(agent)
            c = Claim(fw, agent, targetRoom, targetRoom.start_time)
            claims.append(c)
    print(claims)

    while True:
        for agent in interestedAgents:
            counter = agent.make_counter(fw)
            if counter:
                fw.add_attack(counter.get_attacking(), counter.get_attacked())
            else:
                interestedAgents.remove(agent)
        winning = [claim for claim in claims if fw.is_grounded(claim)]
        winner = random.choice(winning)
        break

    # Reset agents course claiming state
    for agent in agents:
        agent.active_course = None

    return winner

#Check if the room is a good option for the agent (only checks if room is big enough and agent doesn't have a room yet for now)
def viableClaim(agent, room):
    class_size = 0
    for course in agent.courses:
        if course.lectures > 0 \
                and room.size >= course.students \
                and course.students > class_size:
            agent.active_course = course
            class_size = course.students
    return class_size != 0

if __name__ == '__main__':
    rooms = rooms.load_rooms('locations.yaml')
    teachers = agent.load_agents('teachers.yaml')

    for teacher in teachers:
        print(teacher)

    print('')

    for room in rooms:
        print(room)

    for room in rooms:
        print(room)
        debateRoom(room, teachers)
