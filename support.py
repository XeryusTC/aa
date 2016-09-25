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
    arguments = []
 
    #Check if agent can make a claim, and if it can, make it.
    for agent in agents:
        if viableClaim(agent, targetRoom, settledAgents):
            interestedAgents.append(agent)
            c = Claim(fw, agent, targetRoom, targetRoom.get_start_time)
            claims.append(c)
    print(claims)

    #Make an argument why you should have the room (only makes a size argument for now)
    for agent in interestedAgents:
        a = SizeArgument(fw, agent, targetRoom, agent.get_students)
        arguments.append(a)
    print(arguments)

    #Make counter arguments 
    for agent in interestedAgents:
        for argument in arguments:
            if argument.get_owner == agent:
                print('Im breaking')
                break
            else:
                print('Im not breaking')   

    print('done with debate for this room')

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


 

	
