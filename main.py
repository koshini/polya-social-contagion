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

NODE_COUNT = 10
ITERATIONS = 100
AVG_NETWORK_INFECTION = []

def main():
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'edges': 2,
        'red': 500,
        'black': 500,
        'red_budget': 50,
        'black_budget': 50,
        'dist': 'equal',
        'type': 'barabasi'
    }
    
    network = NetWorkHelper(network_initial_condition)
    delta_r = 1
    delta_b = 1
    budget = delta_r * NODE_COUNT
    # set up initial budget distribution
    y = [0]*NODE_COUNT
    y[1] = budget

    G = network.create_network()
    set_positions(G)
    pylab.show()
    pylab.ion()
    fig = plt.figure(figsize=(16,6))
    network_infection_sum = 0
    for node in G.node.items():
        network.construct_super_urn(node)
        network_infection_sum += node[1]['super_urn']['network_infection']
    AVG_NETWORK_INFECTION.append(network_infection_sum / NODE_COUNT)

    
    for i in range(0, ITERATIONS):
        run_time_step(G, network)
        update_fig(G, fig)
        pylab.ioff()
    plt.show()


def run_time_step(G, network, cur_time=0):
    current_conditions = {}
    network_infection_sum = 0
    # total_balls = 0
    for node in G.node.items():
        # network.gradient_descent()
        balls = network.centrality_ratio_strat(node)
        draw = draw_from_superurn(G, network, node)
        current_conditions[node[0]] = draw
        add_balls_to_node(G, network, node[0])
        network_infection_sum += node[1]['super_urn']['network_infection']
        # total_balls += balls

    # print(total_balls) # check if total_balls = budget

    AVG_NETWORK_INFECTION.append(network_infection_sum / NODE_COUNT)


def draw_from_superurn(G, network, node):
    super_urn = network.construct_super_urn(node)
    node[1]['prev_draw'] = find_condition(super_urn)
    return node[1]['prev_draw']


def add_balls_to_node(G, network, node_index):
    print(network.black_dist)
    if (G.node[node_index]['prev_draw'] == 1):
        G.node[node_index]['urns']['red'] += network.red_dist[node_index]
    elif (G.node[node_index]['prev_draw'] == 0):
        G.node[node_index]['urns']['black'] += network.black_dist[node_index]


def find_condition(super_urn):
    red = super_urn['red']
    black = super_urn['black']
    return choice([0, 1], 1, p=[black / (red + black), red / (red + black)])[0]


def update_fig(G, fig):
    pylab.clf()
    gs = fig.add_gridspec(16, 16)
    ax0 = fig.add_subplot(gs[:, :7])
    ax1 = fig.add_subplot(gs[:, 9:])
    color_map = infection_rate_to_color(G)
    nx.draw(G, nx.get_node_attributes(G, 'pos'), ax0, node_color=color_map, linewidths=1, edgecolors='black',
                     cmap=plt.cm.RdGy)

    ax1.plot(list(range(len(AVG_NETWORK_INFECTION))), AVG_NETWORK_INFECTION, color='green', marker='o', markersize=1)
    ax1.set_ylabel('Average Network Infection Rate')
    ax1.set_xlabel('Time')
    ax1.set_xlim([0, ITERATIONS])
    ax1.set_ylim([0.2, 0.6])
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
