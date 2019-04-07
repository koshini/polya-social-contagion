import networkx as nx
import operator
from numpy.random import choice
from network_helper import NetWorkHelper
from graph_generator import get_graph
import matplotlib.pyplot as plt
import csv


def simulate(folder, topology, red_mult, black_mult, strat_dict, iterations, runs, targets=None, initial_condition=None, prefix=None):
    infection_csv = folder + '/empirical-infection' + topology + strat_dict['red_strat'] + strat_dict['black_strat'] + 'infection.csv'
    waste_csv = folder +'/'+ topology + strat_dict['red_strat'] + strat_dict['black_strat'] + 'waste.csv'
    if prefix:
        infection_csv = folder + topology + prefix + strat_dict['red_strat'] + strat_dict[
            'black_strat'] + 'infection.csv'
        # waste_csv = folder + '/' + prefix + strat_dict['red_strat'] + strat_dict['black_strat'] + 'waste.csv'
    for i in range(runs):
        # print(i)
        infection_array, waste_array = simulate_network_infection(folder, topology, red_mult, black_mult, strat_dict, iterations, initial_condition=initial_condition)
        with open(infection_csv, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(infection_array)

        # with open(waste_csv, 'a') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(waste_array)


def simulate_network_infection(folder, topology, red_mult, black_mult, strat_dict, iterations, targets=None, initial_condition=None):
    G = get_graph(folder, topology, red_mult, black_mult, initial_condition=initial_condition, strat=strat_dict)
    network = NetWorkHelper(strat_dict, G, targets)
    infection_array = []
    waste_array = []
    for i in range(0, iterations):
        run_time_step(network, infection_array, waste_array)
    return infection_array, waste_array


def run_time_step(network, infection_array, waste_array):
    network_infection_sum = 0
    waste = 0
    G = network.G

    network.run_time_step()
    for node in G.node.items():
        draw = draw_from_superurn(network, node)
        # Actual infection
        network_infection_sum += draw
        add_balls_to_node(network, node[0])
        # Conditional prob. of the node being infected next time
        # network_infection_sum += node[1]['super_urn']['network_infection']
        if draw == 1:
            waste += network.black_dist[node[0]]

    average_infection = network_infection_sum / network.node_count
    average_waste = waste / network.node_count
    infection_array.append(average_infection)
    waste_array.append(average_waste)


def add_balls_to_node(network, node_index):
    G = network.G
    if (G.node[node_index]['prev_draw'] == 1):
        G.node[node_index]['urns']['red'] += network.red_dist[node_index]
    elif (G.node[node_index]['prev_draw'] == 0):
        G.node[node_index]['urns']['black'] += network.black_dist[node_index]


def draw_from_superurn(network, node):
    super_urn = network.construct_super_urn(node)
    node[1]['prev_draw'] = find_condition(super_urn)
    return node[1]['prev_draw']


def find_condition(super_urn):
    red = super_urn['red']
    black = super_urn['black']
    return choice([0, 1], 1, p=[black / (red + black), red / (red + black)])[0]


def set_top_central_nodes(G):
    list = sorted(nx.get_node_attributes(G, 'centrality_multiplier').items(), key=operator.itemgetter(1), reverse=True)
    top_index_list = []
    for i in range(int(nx.number_of_nodes(G) / 4)):
        top_index_list.append(list[i][0])
    return top_index_list




if __name__ == "__main__":
    main()