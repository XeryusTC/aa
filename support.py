import random
from ics import Calendar, Event
from datetime import datetime

import rooms
import agent
from argument import *
from argument.claim import Claim
from argument.sizeargument import SizeArgument

class Support:
    def __init__(self):
        self.bullshit = []

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

    print("===Claims===")
    #print claims
    for claim in claims:
        print(claim)
    print("")
    
    for claim1 in claims:
        for claim2 in claims:
            if claim1 != claim2:
                fw.add_attack(claim1, claim2)

    while True:
        for agent in interestedAgents:
            print("Agent: " + agent.get_name())
            counter = agent.make_counter(fw, targetRoom)
            print("Counter: " + str(counter))
            if counter:
                fw.add_attack(counter.attacker, counter.attackee)
            print("")
        winning = [claim for claim in claims if fw.is_grounded(claim)]
        break

    if winning:
        winner = random.choice(winning) # TODO: some better method of picking winner
        course = winner.owner.active_course
        course.lectures -= 1
    else:
        course = None

    # Reset agents course claiming state
    for agent in agents:
        agent.active_course = None

    return course

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

    print("===Teachers===")
    for teacher in teachers:
        print(teacher.name)
        print("   Courses---")
        for course in teacher.courses:
            print(course)
        print("   Room Preferences---")
        for preference in teacher.room_preferences:
            print(preference)

    print('')

    schedule = []
    for room in rooms:
        print("Debating room:", room)
        course = debateRoom(room, teachers)
        print("Winning course:", course)
        if course:
            schedule.append({'room': room, 'course': course})

    # Write the schedule
    cal = Calendar()
    today = datetime.today().strftime('%Y-%m-%d')
    for slot in schedule:
        e = Event()
        e.name = "{room} {course_name}".format(room=slot['room'].name,
                course_name=slot['course'].name)
        print("{}T{:0>2}:00:00".format(today, slot['room'].start_time))
        e.begin = "{}T{:0>2}:00:00".format(today, slot['room'].start_time)
        e.end   = "{}T{:0>2}:00:00".format(today, slot['room'].end_time)
        cal.events.append(e)

    with open('schedule.ics', 'w') as f:
        f.writelines(cal)
