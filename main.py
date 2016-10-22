import random
from datetime import datetime
from unipath import Path
import networkx.drawing.nx_pydot
from pydotplus import graphviz
import sys

import rooms
import agent
from schedule import Schedule
from argument import *
from argument.claim import Claim

class Support:
    def __init__(self):
        self.bullshit = []


def write_graph_as_image(path, filename, fw):
    if '--write-image' not in sys.argv:
        return
    path.mkdir(True)
    out = path.child(str(filename))
    fw.write_dot(out + '.dot')
    g = graphviz.graph_from_dot_file(out + '.dot')
    g.write_png(out + '.png')

def debateRoom(targetRoom, agents, room_path):
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
    write_graph_as_image(room_path, 'claims', fw)

    new_arguments = True
    i = 0
    while new_arguments:
        new_arguments = False
        for agent in interestedAgents:
            print("Agent: " + agent.get_name())
            counter = agent.make_counter(fw, targetRoom)
            print("Counter: " + str(counter))
            if counter:
                new_arguments = True
                if counter.type == "attack":
                    fw.add_attack(counter.attacker, counter.attackee)
                elif counter.type == "support":
                    fw.add_support(counter.attacker, counter.attackee)
                elif counter.type == "undercut":
                    fw.add_undercut(counter.attacker, counter.attackee)
            print("")
        winning = [claim for claim in claims if fw.is_grounded(claim)]
        write_graph_as_image(room_path, i, fw)
        i += 1

    if winning:
        winner = random.choice(winning).owner # TODO: some better method of picking winner
        course = winner.has_won(targetRoom)
    else:
        course = None
        winner = None
    print(winner, course)

    # Reset agents course claiming state
    for agent in agents:
        agent.active_course = None

    return course, winner

def viableClaim(agent, room):
    # Check if the agent is free
    if not agent.is_free(room.day, room.start_time, room.end_time):
        return False

    #Check if the room is a good option for the agent (only checks if room
    #is big enough and agent doesn't have a room yet for now)
    class_size = 0
    for course in agent.courses:
        if course.lectures > 0 \
                and room.size >= course.students \
                and course.students > class_size\
                and room.beamer >= course.beamer:
            agent.active_course = course
            class_size = course.students
    return class_size != 0

def print_not_scheduled(agents):
    any_failure = False
    print('Failed to schedule:')
    for agent in agents:
        failure = False
        for course in agent.courses:
            if course.lectures > 0:
                if not failure:
                    print(" " * 4, agent.name)
                print(" " * 8, course.name)
                failure = True
        any_failure |= failure
    if not any_failure:
        print("None")

if __name__ == '__main__':
    rooms = rooms.load_rooms('locations.yaml')
    teachers = agent.load_agents('teachers.yaml')
    out_path = Path('/tmp/arguingagents/' + str(datetime.now()))

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

    schedule = Schedule()

    for room in rooms:
        print("Debating room:", room)
        room_path = out_path.child('{}.{}.{}-{}'.format(room.day, room.name,
            room.start_time, room.end_time))
        course, agent = debateRoom(room, teachers, room_path)
        print("Winning course:", course)
        if course:
            schedule.add(room, course, agent)

    print('========')
    tex = schedule.as_tex_multi_table()
    with open('/tmp/schedule.tex', 'w') as f:
        f.write(tex)
    print(tex)
    print(schedule.as_plain())

    print('========')
    print_not_scheduled(teachers)
