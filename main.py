import networkx as nx
import random
import math
import time
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from numpy.random import choice
import pylab
from matplotlib.pyplot import pause
from network_helper import NetWorkHelper

NODE_COUNT = 3
ITERATIONS = 50
RUNS = 10 #run the same strategy 10 times to get a smooth curve


def main():
    ##### Scenario 1: black: gradient, red: uniform
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'edges': 2,
        'red': 300,
        'black': 300,
        'red_budget': 30,
        'black_budget': 30,
        'red_strat': 'uniform',
        'black_strat': 'gradient',
        'dist': 'equal',
        'type': 'barabasi'
    }

    network = NetWorkHelper(network_initial_condition)
    G = network.create_network()
    infection_rate_1 = run_multiple_simulations(G, network)

    ##### Scenario 2: black: uniform, red: gradient
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'edges': 2,
        'red': 300,
        'black': 300,
        'red_budget': 30,
        'black_budget': 30,
        'red_strat': 'gradient',
        'black_strat': 'uniform',
        'dist': 'equal',
        'type': 'barabasi'
    }

    network = NetWorkHelper(network_initial_condition)
    G = network.create_network()
    infection_rate_2 = run_multiple_simulations(G, network)


    ##### Scenario 3: both gradient
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'edges': 2,
        'red': 300,
        'black': 300,
        'red_budget': 30,
        'black_budget': 30,
        'red_strat': 'gradient',
        'black_strat': 'gradient',
        'dist': 'equal',
        'type': 'barabasi'
    }

    network = NetWorkHelper(network_initial_condition)
    G = network.create_network()
    infection_rate_3 = run_multiple_simulations(G, network)

    # plt.plot(list(range(ITERATIONS)), infection_rate_1)
    # plt.plot(list(range(ITERATIONS)), infection_rate_2)
    plt.plot(list(range(ITERATIONS)), infection_rate_3)
    # plt.legend(['r, b*', 'r*, b', 'r*, b*'], loc='upper left')
    plt.axis([0,ITERATIONS , 0, 1])
    plt.show()

def run_multiple_simulations(G, network):
    arrays_of_infection_rate = []
    for i in range(RUNS):
        print(i)
        infection_array = simulate_network_infection(G, network)
        arrays_of_infection_rate.append(infection_array)

    average_infection_rate_overtime = []
    for t in range(ITERATIONS):
        sum = 0
        for i in range(len(arrays_of_infection_rate)):
            sum += arrays_of_infection_rate[i][t]
        average = sum / len(arrays_of_infection_rate)
        average_infection_rate_overtime.append(average)

    print(average_infection_rate_overtime)
    return average_infection_rate_overtime


def simulate_network_infection(G, network):
    set_positions(G)
    infection_array = []
    # pylab.show()
    # pylab.ion()
    # fig = plt.figure(figsize=(16, 6))
    for node in G.node.items():
        network.construct_super_urn(node)
    for i in range(0, ITERATIONS):
        run_time_step(G, network, infection_array)
        # update_fig(G, fig)
        # pylab.ioff()

    # update_fig(G, fig, infection_array)
    # plt.show()
    return infection_array


def run_time_step(G, network, infection_array):
    current_conditions = {}
    network_infection_sum = 0
    # total_balls = 0

    network.run_time_step()
    for node in G.node.items():
        draw = draw_from_superurn(G, network, node)
        current_conditions[node[0]] = draw
        add_balls_to_node(G, network, node[0])
        network_infection_sum += node[1]['super_urn']['network_infection']

    average_infection = network_infection_sum / NODE_COUNT
    infection_array.append(average_infection)


def draw_from_superurn(G, network, node):
    super_urn = network.construct_super_urn(node)
    node[1]['prev_draw'] = find_condition(super_urn)
    return node[1]['prev_draw']


def add_balls_to_node(G, network, node_index):
    if (G.node[node_index]['prev_draw'] == 1):
        G.node[node_index]['urns']['red'] += network.red_dist[node_index]
    elif (G.node[node_index]['prev_draw'] == 0):
        G.node[node_index]['urns']['black'] += network.black_dist[node_index]


def find_condition(super_urn):
    red = super_urn['red']
    black = super_urn['black']
    return choice([0, 1], 1, p=[black / (red + black), red / (red + black)])[0]


def update_fig(G, fig, infection_array):
    pylab.clf()
    gs = fig.add_gridspec(16, 16)
    ax0 = fig.add_subplot(gs[:, :7])
    ax1 = fig.add_subplot(gs[:, 9:])
    color_map = infection_rate_to_color(G)
    nx.draw(G, nx.get_node_attributes(G, 'pos'), ax0, node_color=color_map, linewidths=1, edgecolors='black',
                     cmap=plt.cm.RdGy)

    ax1.plot(list(range(len(infection_array))), infection_array, color='green', marker='o', markersize=1)
    ax1.set_ylabel('Average Network Infection Rate')
    ax1.set_xlabel('Time')
    ax1.set_xlim([0, ITERATIONS])
    ax1.set_ylim([0, 1])
    pylab.draw()
    pause(0.001)


def set_positions(G):
    pos = nx.spring_layout(G)
    for n, p in pos.items():
        G.node[n]['pos'] = p


def infection_rate_to_color(G):
    color_map = []
    for node in G.node.items():
        infection_rate = node[1]['super_urn']['network_infection']
        color_map.append(1-infection_rate)
    return color_map

def set_color(G):
    color_map = []
    for node in G.node.items():
        if node[1]['prev_draw'] == 1:
            color_map.append('red')
        else:
            color_map.append('black')
    return color_map


if __name__ == "__main__":
    main()
