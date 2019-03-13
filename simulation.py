import networkx as nx
from numpy.random import choice
from network_helper import NetWorkHelper
from graph_generator import get_graph
import matplotlib.pyplot as plt


def main():
    labels = []
    topology = 'meetup'
    G = get_graph(topology)

    # G = nx.barabasi_albert_graph(100, 2)
    iterations = 500
    runs = 1
    node_count = nx.number_of_nodes(G)
    red_budget = node_count * 10
    black_budget = node_count * 10


    # uniform vs centrality
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot_strat',
        'black_strat': 'follow_bot',
    }

    labels.append(strat_dict['red_strat'])
    labels.append(strat_dict['black_strat'])

    infection_rate_1 = simulate(topology, strat_dict, iterations, runs)

###############################################################################################
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'bot_strat',
        'black_strat': 'uniform',
    }

    labels.append(strat_dict['red_strat'])
    labels.append(strat_dict['black_strat'])

    infection_rate_2 = simulate(topology, strat_dict, iterations, runs)

###############################################################################################
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'entropy',
    }

    # labels.append(strat_dict['red_strat'])
    # labels.append(strat_dict['black_strat'])
    #
    # infection_rate_3 = simulate(topology, strat_dict, iterations, runs)

###############################################################################################
    strat_dict = {
        'red_budget': red_budget,
        'black_budget': black_budget,
        'red_strat': 'uniform',
        'black_strat': 'centrality',
    }

    # labels.append(strat_dict['red_strat'])
    # labels.append(strat_dict['black_strat'])
    #
    # infection_rate_4 = simulate(topology, strat_dict, iterations, runs)



    plt.plot(list(range(iterations)), infection_rate_1, label='red: ' + labels[0] + ', black: ' + labels[1])
    plt.plot(list(range(iterations)), infection_rate_2, label='red: ' + labels[2] + ', black: ' + labels[3])
    # plt.plot(list(range(iterations)), infection_rate_3, label='red: ' + labels[4] + ', black: ' + labels[5])
    # plt.plot(list(range(iterations)), infection_rate_4, label='red: ' + labels[6] + ', black: ' + labels[7])
    plt.legend(loc='upper left')
    plt.axis([0,iterations, 0, 0.9])
    title = topology + ' network'
    plt.title(title)
    filename = title + '-' + str(labels) + '.png'
    plt.savefig(filename, bbox_inches='tight')
    # plt.show()
    print()


def simulate(topology, strat_dict, iterations, runs):
    arrays_of_infection_rate = []
    for i in range(runs):
        print('simulate run: ' + str(i))
        infection_array = simulate_network_infection(topology, strat_dict, iterations)
        arrays_of_infection_rate.append(infection_array)

    average_infection_rate_overtime = []
    for t in range(iterations):
        sum = 0
        for i in range(len(arrays_of_infection_rate)):
            sum += arrays_of_infection_rate[i][t]
        average = sum / len(arrays_of_infection_rate)
        average_infection_rate_overtime.append(average)

    return average_infection_rate_overtime


def simulate_network_infection(topology, strat_dict, iterations):
    G = get_graph(topology)
    network = NetWorkHelper(strat_dict, G)
    G = network.G
    infection_array = []
    for i in range(0, iterations):
        print(i)
        run_time_step(network, infection_array)
    return infection_array


def run_time_step(network, infection_array):
    current_conditions = {}
    network_infection_sum = 0
    G = network.G

    network.run_time_step()
    for node in G.node.items():
        draw = draw_from_superurn(network, node)
        current_conditions[node[0]] = draw
        add_balls_to_node(network, node[0])
        network.construct_super_urn(node)
        network_infection_sum += node[1]['super_urn']['network_infection']

    network.record_entropy()
    average_infection = network_infection_sum / network.node_count
    infection_array.append(average_infection)


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


if __name__ == "__main__":
    main()