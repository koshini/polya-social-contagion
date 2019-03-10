import networkx as nx
from numpy.random import choice
from network_helper import NetWorkHelper
from graph_generator import get_graph
import matplotlib.pyplot as plt


def main():
    G = get_graph('facebook')
    # G = nx.barabasi_albert_graph(100, 2)
    iterations = 200
    node_count = nx.number_of_nodes(G)
    budget = node_count * 10


    # uniform vs centrality
    strat_dict = {
        'red_budget': budget,
        'black_budget': budget,
        'red_strat': 'uniform',
        'black_strat': 'gradient',
    }

    # initial_balls = node_count * 50
    # initial_condition = {
    #     'node_count': node_count,
    #     'parameter': 2,
    #     'red': initial_balls,
    #     'black': initial_balls,
    #     'dist': 'random',
    # }

    network_centrality = NetWorkHelper(strat_dict, G)
    # network_centrality.create_network(initial_condition)
    # network_centrality.set_centrality_mult()
    network_infection_centrality = []
    for i in range(0, iterations):
        print(i)
        run_time_step(network_centrality, network_infection_centrality)
        print()

    # uniform vs uniform
    G = get_graph('facebook')
    # G = nx.barabasi_albert_graph(100, 2)
    strat_dict = {
        'red_budget': budget,
        'black_budget': budget,
        'red_strat': 'uniform',
        'black_strat': 'uniform',
    }
    network_uniform = NetWorkHelper(strat_dict, G)
    # network_uniform.create_network(initial_condition)
    # network_uniform.set_centrality_mult()


    network_infection_uniform = []
    for i in range(0, iterations):
        print(i)
        run_time_step(network_uniform, network_infection_uniform)
        print()

    plt.plot(list(range(iterations)), network_infection_centrality, label='uniform vs. gradient descent')
    plt.plot(list(range(iterations)), network_infection_uniform, label='uniform vs. uniform')
    plt.title('Facebook Network')
    plt.legend()
    plt.show()
    print()


def run_time_step(network, infection_array):
    current_conditions = {}
    network_infection_sum = 0
    G = network.G

    network.run_time_step()
    i = 0
    for node in G.node.items():
        draw = draw_from_superurn(network, node)
        current_conditions[node[0]] = draw
        add_balls_to_node(network, node[0], i)
        network.construct_super_urn(node)
        network_infection_sum += node[1]['super_urn']['network_infection']
        i += 1

    network.record_entropy()
    average_infection = network_infection_sum / network.node_count
    infection_array.append(average_infection)

def add_balls_to_node(network, node_index, i):
    G = network.G
    if (G.node[node_index]['prev_draw'] == 1):
        G.node[node_index]['urns']['red'] += network.red_dist[i]
    elif (G.node[node_index]['prev_draw'] == 0):
        G.node[node_index]['urns']['black'] += network.black_dist[i]


def draw_from_superurn(network, node):
    super_urn = network.construct_super_urn(node)
    node[1]['prev_draw'] = find_condition(super_urn)
    return node[1]['prev_draw']


def find_condition(super_urn):
    red = super_urn['red']
    black = super_urn['black']
    return choice([0, 1], 1, p=[black / (red + black), red / (red + black)])[0]


if __name__ == "__main__":
    main()