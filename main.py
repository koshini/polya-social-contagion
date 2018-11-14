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
AVG_NETWORK_INFECTION = []

def main():
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'edges': 2,
        'red': 100,
        'black': 100,
        'dist': 'equal'
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
    #perform all derivatives for each node

    for r in range(0,NODE_COUNT):
        # expected network exposure at time n-1, proportion of red balls in node i's superurn after n-1 draws
        S[i][n - 1] = (U[i][n] * X[j][n]) / X[j][n]
        Constant = (G.node['super_urn']['red'] + delta_r*S[i][n-1] + delta_r)/((G.node['super_urn']['red'] + delta_r*S[i][n-1] + delta_r) + delta_b + delta_b(1-))


        X[j][n] = (G.node['super_urn']['red'] + G.node['super_urn']['black']) + delta_r+(1-)*delta_b
        partial_deriv[r] = (1/NODE_COUNT)*Constant*(1/(1-(G.node['urns']['red'] + delta_r)/((G.node['urns']['red']+G.node['urns']['black'])+ delta_r + (1-)*delta_b)*X/X

    
    i = numpy.min(partial_deriv)
    #move only in that direction

    y_bar =[0] * NODE_COUNT
    y_bar[i] = budget
    gamma = 0.5


    #define the function to determine step size


    #porportion of red balls in node i's urn after n'th draw
    U[i][n] = (G.node['urns']['red'] + delta_r)/(G.node['urns']['red']+G.node['urns']['black'])+ delta_r + (1-)*delta_b


    for i in range(0,NODE_COUNT)
        C[i] = G.node['urns']['red'] + delta_r*S[i][n-1] + delta_r
        D[i] = C[i] + G.node['urns']['black'] + delta_b*(1-)
        sigma[i] = (y-gamma(y_bar-y))*(1-S[i][n-1])
        Fn[i] = (1/NODE_COUNT)*C[i]/(D[i] + sigma[i])

    alpha_k = numpy.min(Fn)
    y[i+1] = y[i]+ alpha_k(y_bar[i] + y[i])

    delta_b = y[i+1]

    return delta_b




def run_time_step(G, delta_r, delta_b, cur_time=0):
    current_conditions = {0: 0}
    network_infection_sum = 0
    for node in G.node.items():
        add_balls_to_node(G, node[0], delta_r, delta_b)
        draw = draw_from_superurn(G, node)
        current_conditions[node[0]] = draw
        network_infection_sum += node[1]['super_urn']['network_infection']

    average_network_infection = network_infection_sum / NODE_COUNT
    AVG_NETWORK_INFECTION.append(average_network_infection)


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
