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

NODE_COUNT = 4
AVG_NETWORK_INFECTION = []

def main():
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'edges': 1,
        'red': 50,
        'black': 50,
        'red_budget': 10,
        'black_budget': 10,
        'dist': 'equal',
        'type': 'path'
    }
    
    network = NetWorkHelper(network_initial_condition)
    iterations = 50
    delta_r = 3
    delta_b = 1
    budget = delta_r * NODE_COUNT
    # set up initial budget distribution
    y = [0]*NODE_COUNT
    y[1] = budget

    G = network.create_network()
    set_positions(G)
    pylab.show()
    pylab.ion()

    # print("Initial network distribution:")
    # for node in G.node.items():
    # print(node[0], "red:", node[1]['urns']['red'], "black", node[1]['urns']['black'])
    # print("\n")


    for i in range(0, iterations):

        # delta_b = gradient_descent(G)

        run_time_step(G, delta_r, delta_b)
        update_fig(G)
        pylab.ioff()

    # Plot average network infection over time
    plt.figure(2)
    plt.plot(list(range(iterations)), AVG_NETWORK_INFECTION, color='green', marker='o', markersize=3)
    plt.ylabel('average network exposure')
    plt.xlabel('time')
    plt.show()


# TODO: use gradient descent algorithm to determine delta_b
def gradient_descent(G, delta_r, delta_b, budget, y):
    pass
    exposure_rate = {}
    
    for node in G.node.items():
        current_red = 0
        current_black = 0
        expected_red = 0
        expected_black = 0
        
        current_red += node[1]['urns']['red'] 
        current_black += node[1]['urns']['black']
        expected_red += delta_r*node[1]['prev_exposure']
        
        neighbors = nx.all_neighbors(G, node[0])
        for neighbor_node in neighbors:
            current_red += G.node[neighbor_node]['urns']['red'] 
            current_black += G.node[neighbor_node]['urns']['black']
            expected_red += delta_r*G.node[neighbor_node]['prev_exposure']
        
        #TODO: we have all the constants of the equations now, but
        #      from this point we have to do the sum of the partials for each node
        #      and store it.




def run_time_step(G, delta_r, delta_b, cur_time=0):
    current_conditions = {}
    network_infection_sum = 0
    for node in G.node.items():
        draw = draw_from_superurn(G, node)
        current_conditions[node[0]] = draw
        add_balls_to_node(G, node[0], delta_r, delta_b)
        network_infection_sum += node[1]['super_urn']['network_infection']

    AVG_NETWORK_INFECTION.append(network_infection_sum / NODE_COUNT)


def draw_from_superurn(G, node):
    super_urn = construct_super_urn(G, node)
    node[1]['prev_draw'] = find_condition(super_urn)
    return node[1]['prev_draw']


def construct_super_urn(G, node):
    # Construct super urns
    super_urn = {'red': node[1]['urns']['red'], 'black': node[1]['urns']['black']}
    neighbors = nx.all_neighbors(G, node[0])
    for neighbor_node in neighbors:
        super_urn['red'] += G.node[neighbor_node]['urns']['red']
        super_urn['black'] += G.node[neighbor_node]['urns']['black']

    # network_infection(Si,n) = proportion of the red balls in the node's super urn
    network_infection = super_urn['red'] / (super_urn['red'] + super_urn['black'])
    super_urn['network_infection'] = network_infection
    node[1]['super_urn'] = super_urn
    return super_urn


def add_balls_to_node(G, node_index, added_red, added_black):
    if (G.node[node_index]['prev_draw'] == 1):
        G.node[node_index]['urns']['red'] += added_red
    elif (G.node[node_index]['prev_draw'] == 0):
        G.node[node_index]['urns']['black'] += added_black


def find_condition(super_urn):
    red = super_urn['red']
    black = super_urn['black']
    return choice([0, 1], 1, p=[black / (red + black), red / (red + black)])[0]


def update_fig(G):
    pylab.clf()
    color_map = set_color(G)
    nx.draw(G, nx.get_node_attributes(G, 'pos'), node_color=color_map)
    pylab.draw()
    pause(0.1)


def set_positions(G):
    pos = nx.random_layout(G)
    for n, p in pos.items():
        G.node[n]['pos'] = p


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
