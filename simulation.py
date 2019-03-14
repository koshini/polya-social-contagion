import networkx as nx
import operator
from numpy.random import choice
from network_helper import NetWorkHelper
from graph_generator import get_graph
import matplotlib.pyplot as plt
import csv


def main():
    labels = []
    topology = 'facebook'
    G = get_graph(topology)
    targets = set_top_central_nodes(G)


    # G = nx.barabasi_albert_graph(100, 2)
    iterations = 30
    runs = 1
    node_count = nx.number_of_nodes(G)
    red_budget = node_count * 10
    black_budget = node_count * 10


    # uniform vs centrality
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'entropy',
    }

    labels.append(strat_dict['red_strat'])
    labels.append(strat_dict['black_strat'])

    infection_rate_1 = simulate(topology, strat_dict, iterations, runs, targets)

###############################################################################################
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'pure_centrality',
    }

    labels.append(strat_dict['red_strat'])
    labels.append(strat_dict['black_strat'])

    infection_rate_2 = simulate(topology, strat_dict, iterations, runs, targets)

###############################################################################################
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'centrality_ratio',
    }

    labels.append(strat_dict['red_strat'])
    labels.append(strat_dict['black_strat'])

    infection_rate_3 = simulate(topology, strat_dict, iterations, runs, targets)

###############################################################################################
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'centrality_entropy',
    }

    # labels.append(strat_dict['red_strat'])
    # labels.append(strat_dict['black_strat'])
    #
    # infection_rate_4 = simulate(topology, strat_dict, iterations, runs, targets)

###############################################################################################
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'bot',
    }

    # labels.append(strat_dict['red_strat'])
    # labels.append(strat_dict['black_strat'])
    #
    # infection_rate_5 = simulate(topology, strat_dict, iterations, runs, targets)

###############################################################################################
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'gradient',
    }

    # labels.append(strat_dict['red_strat'])
    # labels.append(strat_dict['black_strat'])
    #
    # infection_rate_6 = simulate(topology, strat_dict, iterations, runs, targets)


    # plt.plot(list(range(iterations)), infection_rate_1, label='red: ' + labels[0] + ', black: ' + labels[1])
    # plt.plot(list(range(iterations)), infection_rate_2, label='red: ' + labels[2] + ', black: ' + labels[3])
    # plt.plot(list(range(iterations)), infection_rate_3, label='red: ' + labels[4] + ', black: ' + labels[5])
    # plt.plot(list(range(iterations)), infection_rate_4, label='red: ' + labels[6] + ', black: ' + labels[7])
    # plt.plot(list(range(iterations)), infection_rate_5, label='red: ' + labels[8] + ', black: ' + labels[9])
    # plt.plot(list(range(iterations)), infection_rate_6, label='red: ' + labels[10] + ', black: ' + labels[11])
    # plt.legend(loc='best', prop={'size': 5})
    # plt.axis([0,iterations, 0, 0.9])
    # title = topology + ' network'
    # plt.title(title)
    # filename = title + ' avg emprical infection -' + str(labels) + '.png'
    # plt.savefig(filename, bbox_inches='tight')
    # plt.show()
    print()


def simulate(topology, strat_dict, iterations, runs, targets):
    arrays_of_infection_rate = []
    arrays_of_waste_arrays = []
    infection_csv = 'results/empirical-infection' + topology + strat_dict['red_strat'] + strat_dict['black_strat'] + 'infection.csv'
    waste_csv = 'results/' + topology + strat_dict['red_strat'] + strat_dict['black_strat'] + 'waste.csv'
    for i in range(runs):
        infection_array, waste_array = simulate_network_infection(topology, strat_dict, iterations, targets)
        with open(infection_csv, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(infection_array)

        with open(waste_csv, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(waste_array)

        arrays_of_infection_rate.append(infection_array)
        arrays_of_waste_arrays.append(waste_array)
    #
    # average_infection_rate_overtime = []
    # for t in range(iterations):
    #     sum = 0
    #     for i in range(len(arrays_of_infection_rate)):
    #         sum += arrays_of_infection_rate[i][t]
    #     average = sum / len(arrays_of_infection_rate)
    #     average_infection_rate_overtime.append(average)
    #
    # return average_infection_rate_overtime


def simulate_network_infection(topology, strat_dict, iterations, targets):
    G = get_graph(topology)
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