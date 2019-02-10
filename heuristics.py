from main import run_multiple_simulations, simulate_network_infection, run_time_step, draw_from_superurn, add_balls_to_node, find_condition
from numpy.random import choice
from network_helper import NetWorkHelper
import matplotlib.pyplot as plt
import networkx as nx

NODE_COUNT = 10
ITERATIONS = 100
RUNS = 10

network_initial_condition = {
        'node_count': NODE_COUNT,
        'edges': 2,
        'red': 500,
        'black': 500,
        'red_budget': 50,
        'black_budget': 50,
        'red_strat': 'uniform',
        'black_strat': 'heuristic',
        'dist': 'random',
        'type': 'barabasi',
        'heuristic_param': ['centrality', 'degree', 'infection']
    }


################ all ######################
infection_rate_1 = run_multiple_simulations(network_initial_condition)
plt.plot(list(range(ITERATIONS)), infection_rate_1)


################ centrality ######################
network_initial_condition['heuristic_param'] = ['centrality']
infection_rate_2 = run_multiple_simulations(network_initial_condition)
plt.plot(list(range(ITERATIONS)), infection_rate_2)

################ degree ######################
network_initial_condition['heuristic_param'] = ['degree']
infection_rate_3 = run_multiple_simulations(network_initial_condition)
plt.plot(list(range(ITERATIONS)), infection_rate_3)

################ infection ######################
network_initial_condition['heuristic_param'] = ['infection']
infection_rate_4 = run_multiple_simulations(network_initial_condition)
plt.plot(list(range(ITERATIONS)), infection_rate_4)


plt.legend(['all', 'centrality', 'degree', 'infection'], loc='upper left')

plt.axis([0,ITERATIONS, 0.2, 0.7])
plt.show()

# TODO: implement gullibility parameter
# if one is gullible, then they would change their opinion to either side easily. Model it by having fewer initial balls?