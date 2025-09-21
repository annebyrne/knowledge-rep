from aima.agents4e import *
import numpy


# STATE TRANSITION TABLE
# Farmer (Fa), Fox(Fx), Chicken(C) and Seed(S). Only considers start & end states, doesn't consider boat.
# +-----------------------+----------------------+-------------------+-------------------+-------------------+
# | Current State / Input | move(Fa, C)          | move(Fa)          | move(Fa, Fx)      | move(Fa, S)       |
# +-----------------------+----------------------+-------------------+-------------------+-------------------+
# | Fa, C, Fx, S in LocA  | Fx, S in LocA        |                   |                   |                   |
# |                       | Fa, C in LocB        |                   |                   |                   |
# +-----------------------+----------------------+-------------------+-------------------+-------------------+
# | Fx, S in LocA         |                      | Fa, Fx, S in LocA |                   |                   |
# | Fa, C in LocB         |                      | C in LocB         |                   |                   |
# +-----------------------+----------------------+-------------------+-------------------+-------------------+
# | Fa, Fx, S in LocA     |                      |                   | S in LocA         |                   |
# | C in LocB             |                      |                   | Fa, Fx, C in LocB |                   |
# +-----------------------+----------------------+-------------------+-------------------+-------------------+
# | S in LocA             | Fa, C, S in LocA     |                   |                   |                   |
# | Fa, Fx, C in LocB     | Fx in LocB           |                   |                   |                   |
# +-----------------------+----------------------+-------------------+-------------------+-------------------+
# | Fa, C, S in LocA      |                      |                   |                   | C in LocA         |
# | Fx in LocB            |                      |                   |                   | Fa, Fx, S in LocB |
# +-----------------------+----------------------+-------------------+-------------------+-------------------+
# | C in LocA             |                      | Fa, C in LocA     |                   |                   |
# | Fa, Fx, S in LocB     |                      | Fx, S in LocB     |                   |                   |
# +-----------------------+----------------------+-------------------+-------------------+-------------------+
# | Fa, C in LocA         | Fa, Fx, C, S in LocB |                   |                   |                   |
# | Fx, S in LocB         |                      |                   |                   |                   |
# +-----------------------+----------------------+-------------------+-------------------+-------------------+
# | Fa, Fx, C, S in LocB  |                      |                   |                   |                   |
# +-----------------------+----------------------+-------------------+-------------------+-------------------+

# our agent
def TableDrivenAgentProgram(table):
    def program(percepts):
        action = table.get(tuple(percepts))
        return action

    return program

class FarmerAgent(Agent):
    location = loc_A

def TableDrivenFarmerAgent():
    table = {
        ((loc_A, str(['Farmer', 'Fox', 'Chicken', 'Seed'])),( loc_B, '[]')): 'move_chicken',
        ((loc_A, str(['Fox', 'Seed'])), (loc_B, str(['Chicken', 'Farmer']))): 'move_self',
        ((loc_A, str(['Fox', 'Seed', 'Farmer'])), (loc_B, str(['Chicken']))): 'move_fox',
        ((loc_A, str(['Seed'])), (loc_B, str(['Chicken', 'Fox', 'Farmer']))): 'move_chicken',
        ((loc_A, str(['Seed', 'Chicken', 'Farmer'])), (loc_B, str(['Fox']))): 'move_seed',
        ((loc_A, str(['Chicken'])), (loc_B, str(['Fox', 'Seed', 'Farmer']))): 'move_self',
        ((loc_A, str(['Chicken', 'Farmer'])), (loc_B, str(['Fox', 'Seed']))): 'move_chicken',
        ((loc_A, '[]'), (loc_B, str(['Fox', 'Seed', 'Chicken', 'Farmer']))): 'stop'
    }
    return FarmerAgent(TableDrivenAgentProgram(table))

class TrivialRiverCrossingEnvironment(Environment):
    """This environment has two locations, A and B. Each can host
    up to 4 things, including the agent. The agent perceives its location 
    and the location's members."""

    def __init__(self):
        super().__init__()
        self.locations = {
            loc_A: ['Farmer', 'Fox', 'Chicken', 'Seed'],
            loc_B: []
            }
        print(self.locations)

    def percept(self, agent):
        """Returns the agent's location, and the location members."""
        res = []
        for key, val in self.locations.items():
            res.append((key, str(val)))
        return (*res,)
    
    def update_agent_location(self, agent):
        self.locations[agent.location].remove('Farmer')
        if agent.location == loc_A:
            self.locations[loc_B].append('Farmer')
            agent.location = loc_B
        else: 
            self.locations[loc_A].append('Farmer')
            agent.location = loc_A

    def update_thing_location(self, agent, thing):
        self.locations[agent.location].remove(thing)
        if agent.location == loc_A:
            self.locations[loc_B].append(thing)
        else: 
            self.locations[loc_A].append(thing)
        self.update_agent_location(agent)

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status"""
        if (action == 'move_self'):
            self.update_agent_location(agent)
        elif action == 'move_chicken':
            self.update_thing_location(agent, 'Chicken')
        elif action == 'move_fox':
            self.update_thing_location(agent, 'Fox')
        elif action == 'move_seed':
            self.update_thing_location(agent, 'Seed')

    def default_location(self, thing):
        return loc_A

farmer = TraceAgent(TableDrivenFarmerAgent())
environment = TrivialRiverCrossingEnvironment()
environment.add_thing(farmer, loc_A)
environment.run(20)