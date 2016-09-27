import rooms
import agent
from argument import *
from argument.claim import Claim
from argument.sizeargument import SizeArgument

class Support:
    def __init__(self):
        bullshit = []    
        
def debateRoom(targetRoom, agents, settledAgents):
    interestedAgents = []
    claims = []
    fw = ArgumentationFramework() 
 
    #Check if agent can make a claim, and if it can, make it.
    for agent in agents:
        if viableClaim(agent, targetRoom, settledAgents):
            interestedAgents.append(agent)
            c = Claim(fw, agent, targetRoom, targetRoom.start_time)
            claims.append(c)
    print(claims)
    
    while True:
        for agent in interestedAgents:
            counter = agent.makeCounter(fw)
            if counter:
                fw.add_attack(counter.get_attacking(), counter.get_attacked())
            else:
                interestedAgents.remove(agent)
        winning = [claim for claim in claims if fw.is_grounded(claim)]
        winner = random.choice(winning)
        break
    return winner
    
#Check if the room is a good option for the agent (only checks if room is big enough and agent doesn't have a room yet for now)
def viableClaim(targetAgent, targetRoom, settledAgents):
    viableOption = False
    
    if (targetRoom.size >= targetAgent.students and ((targetAgent in settledAgents) == False)):
        viableOption = True
    print(viableOption)
    return viableOption

if __name__ == '__main__':
    rooms = rooms.load_rooms('locations.yaml')
    teachers = agent.load_agents('teachers.yaml')

    for teacher in teachers:
        print(teacher)
    
    print('')

    for room in rooms:
        print(room)

    fw = ArgumentationFramework() 
    settledAgents = []
    
    for room in rooms:
        print(room)
        debateRoom(room, teachers, settledAgents)


 

    
