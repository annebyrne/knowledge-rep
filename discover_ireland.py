# Discover Ireland - Uninformed search
import pandas
import networkx as nx
import matplotlib.pyplot as plt
from aima.search import *


geo_data = pandas.read_csv('cities_ie.csv', index_col=0, header=0)
distances = geo_data.to_dict('index')
# distances = list(geo_data.stack().to_dict().items())

# d = { 'a': 1, 'b': 2, 'c': 3 }
# list(d.items()) ->  [('a', 1), ('c', 3), ('b', 2)]
# [(v, k) for k, v in d.items()] -> [(1, 'a'), (3, 'c'), (2, 'b')]




# RouteProblem()

distance_graph = UndirectedGraph(distances)
print("we built the graph woohoo!")
visual = nx.Graph(distances)
nx.draw(visual, with_labels=True, font_weight='bold')
plt.savefig("filename.png")

# EXERCISE 1
# Generate a graph based representation of Irish towns, cities & villages 
# that adheres to the following requirements.
#   1) Contains at least 15 nodes.
#   2) At least 5 nodes have a branching factor of 3.
#   3) At least one path with a depth of 8.


# EXERCISE 2
# Generate three problem statements that will be used to
# evaluate the uninformed search strategies. These should
# be designed to demonstrate some property of the search
# approach which you found interesting - briefly discuss.


# EXERCISE 3
# Compare the following search approaches performance:
# • breadth_first_tree_search
# • breadth_first_graph_search
# • depth_first_tree_search
# • depth_first_graph_search
# • depth_limited_search
# • iterative_deepening_search
# • biderectional_search
# Use the functionality made available by “search.py”/“search4e.py” 
# in order to compare the approaches. Provide a table of results for each problem
# statement and a rationale as the primary differentiation between graph and tree based approaches. 
# Similarly discuss the pro’s con’s of each approach from your understanding 
# of the theory and experimental validation.
