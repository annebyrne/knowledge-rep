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

#  QUESTION 2
#  PEAS Table
# +------------------------+----------------------+--------------+-----------------------------+------------------------------------------+
# | Agent Type             | Performance          | Environment  | Actuators                   | Sensors                                  |
# |                        | Measure              |              |                             |                                          |
# +------------------------+----------------------+--------------+-----------------------------+------------------------------------------+
# | RandomVacuumAgent      | Ratio of clean tiles | 2 tile world | Move left or right (wheels) | None (ignored)                           |
# |                        | to moves made        |              | Suck up dirt (vacuum hose)  |                                          |
# +------------------------+----------------------+--------------+-----------------------------+------------------------------------------+
# | TableDrivenVacuumAgent | Ratio of clean tiles | 2 tile world | Move left or right (wheels) | Location, Status of tile (clean / dirty) |
# +------------------------+----------------------+--------------+-----------------------------+------------------------------------------+
# |                        | to moves made        |              | Suck up dirt (vacuum hose)  | Hardcoded in advance                     |
# | ReflexVacuumAgent      | Ratio of clean tiles | 2 tile world | Move left or right (wheels) | Location, Status of tile (clean / dirty) |
# |                        | to moves made        |              | Suck up dirt (vacuum hose)  | Reactive to immediate input              |
# +------------------------+----------------------+--------------+-----------------------------+------------------------------------------+
# | ModelBasedVacuumAgent  | Ratio of clean tiles | 2 tile world | Move left or right (wheels) | Location, Status of tile (clean / dirty) |
# |                        | to moves made        |              | Suck up dirt (vacuum hose)  | Prior knowledge of world                 |
# +------------------------+----------------------+--------------+-----------------------------+------------------------------------------+

# Comparative Analysis
test_agents = [RandomVacuumAgent, TableDrivenVacuumAgent, ReflexVacuumAgent, ModelBasedVacuumAgent]
environment = TrivialVacuumEnvironment
analysis = compare_agents(environment, test_agents, 24, 1000)
results = {
    tup[0].__name__: tup[1] for tup in analysis
}
print(results)

max_score = max(results.values())
min_score = min(results.values())

best_performer = [key for key in results if results[key] == max_score]
worst_performer = [key for key in results if results[key] == min_score]

print(f"best performance was {best_performer} with {max_score}")
print(f"worst performance was {worst_performer} with {min_score}")

# Agent Performance
# RandomVacuumAgent ignores all its percepts and so this results in poor performance,
# as it will move regardless of the tile status. This can mean many needless moves.
# However it doesn't perform as poorly as ReflexVacuumAgent. ReflexVacuumAgent can get
# stuck in a loop as it is only concerned with the current state, and doesn't have 
# the ability to make a Noop action like ModelBasedVacuumAgent. In comparison to 
# RandomVacuumAgent, it doesn't have the ability to make a random choice to break
# out of the loop.
# TableDrivenVacuumAgent & ModelBasedVacuumAgent both take into account the history
# of the world, ModelBasedVacuumAgent does this by maintaining internal state whereas 
# TableDrivenVacuumAgent has the actions hardcoded ahead of time in its percept sequence.

# QUESTION 3
class OneDimensionalVacuumEnvironment(VacuumEnvironment):
    def __init__(self, width=10):
        super().__init__(width, 0)
        self.add_walls()

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent, ModelBasedVacuumAgent]
    
    def add_walls(self):
        self.add_thing(Wall(), (0, 0))
        self.add_thing(Wall(), (self.width - 1, 0))
        # Updates iteration start and end (with walls).
        self.x_start, self.y_start = (1, 0)
        self.x_end, self.y_end = (self.width - 1, 0)

    def execute_action(self, agent, action):
        agent.bump = False
        if action == 'Suck':
            dirt_list = self.list_things_at(agent.location, Dirt)
            if dirt_list != []:
                dirt = dirt_list[0]
                agent.performance += 100
                self.delete_thing(dirt)
        elif action == 'Forward':
            x, y = agent.location
            agent.bump = self.move_to(agent, (x + 1, 0))

        if action != 'NoOp':
            agent.performance -= 1



def OneDimRandomVacuumAgent():
    return Agent(RandomAgentProgram(['Forward', 'Suck', 'NoOp']))

def OneDimReflexVacuumAgent():
    def program(percept):
        status, obstacle = percept
        if status == 'Dirty':
            return 'Suck'
        elif status == 'Clean' and obstacle == 'None':
            return 'Forward'
        elif status == 'Clean' and obstacle == 'Bump':
            return 'Noop'
    return Agent(program)

def OneDimModelBasedVacuumAgent():
    model = []

    def program(percept):
        status, obstacle = percept
        model.append(obstacle)
        if model.count('Bump') == 2:
            return 'Noop'
        elif status == 'Clean' and obstacle == 'Bump':
            return 'NoOp'
        elif status == 'Dirty':
            return 'Suck'
    return Agent(program)

one_dim_agents = [OneDimRandomVacuumAgent, OneDimReflexVacuumAgent, OneDimModelBasedVacuumAgent]
one_dim_environment = OneDimensionalVacuumEnvironment
one_dim_analysis = compare_agents(one_dim_environment, one_dim_agents)
print(one_dim_analysis)
one_dim_results = {
    tup[0].__name__: tup[1] for tup in one_dim_analysis
}
print(one_dim_results)

one_dim_max_score = max(one_dim_results.values())
one_dim_min_score = min(one_dim_results.values())

best = [key for key in one_dim_results if one_dim_results[key] == one_dim_max_score]
worst = [key for key in one_dim_results if one_dim_results[key] == one_dim_min_score]

print(f"best performance was {best} with {one_dim_max_score}")
print(f"worst performance was {worst} with {one_dim_min_score}")