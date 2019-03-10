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
import csv

NODE_COUNT = 100 
ITERATIONS = 500
RUNS = 5 # run the same strategy 10 times to get a smooth curve

def main():
    ##### Scenario 1: black: gradient, red: uniform
    multiple_simulations()
    #single_simulation()

def single_simulation():
    ##### Scenario 1: black: gradient, red: uniform
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'parameter': 3,
        'red': 5000,
        'black': 5000,
        'red_budget': 500,
        'black_budget': 500,
        'red_strat': 'gradient',
        'black_strat': 'centrality',
        'dist': 'random',
        'type': 'barabasi'
    }
    
    network = NetWorkHelper(network_initial_condition)

    G = network.create_network()
    set_positions(G)
    pylab.show()
    pylab.ion()
    #fig = plt.figure(figsize=(16,6))
    #plt.axis([0,ITERATIONS, 0.1, 0.9])
    network_infection_sum = 0
    
    infection_array = []
    for node in G.node.items():
        network.construct_super_urn(node)
        network_infection_sum += node[1]['super_urn']['network_infection']
    infection_array.append(network_infection_sum/NODE_COUNT)
    
    #Open csv logger
    with open('node_data_test.csv', mode='w', newline = '') as node_data:
        data_writer = csv.writer(node_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #Label Nodes
        data_writer.writerow(range(0,NODE_COUNT))
        #Label degree of each node
        degree = []
        for index, node in G.node.items():
            degree.append(G.degree(index))
        data_writer.writerow(degree)
        #Label centrality of each node
        closeness_centrality = list(nx.closeness_centrality(G).values())
        data_writer.writerow(closeness_centrality)
        
        for i in range(0, ITERATIONS):
            #Add black distribution and node infection after each
            network_infection = []
            for node in G.node.items():
                network_infection.append(node[1]['super_urn']['network_infection'])
            data_writer.writerow(network_infection)
            
            run_time_step(G, network, infection_array)
            
            data_writer.writerow(network.black_dist)
            
            #update_fig(G, fig, infection_array)
            #pylab.ioff()
            
        #plt.show()
    
    ave_entropy = []
    entropy_sums = []
    for i in range (0,ITERATIONS+1):
        entropy_sum = 0
        for node in G.node.items():
            entropy_sum += node[1]['centrality_multiplier'] * node[1]['entropy'][i]
        ave_entropy.append(entropy_sum/NODE_COUNT)
        entropy_sums.append(entropy_sum)
        if i > 0:
            continue
            #print(ave_entropy[i]*100 , infection_array[i]*100)
            
    plt.figure(figsize=(16,6))  
    plt.axis([0,ITERATIONS, 0.1, 0.9])
    plt.plot(list(range(ITERATIONS+1)), infection_array)
    plt.show()
    
    #plt.figure(figsize=(16,6))
    #plt.plot(list(range(ITERATIONS+1)), ave_entropy)
    #plt.show()
    
    #plt.figure(figsize=(16,6))
    #plt.plot(list(range(ITERATIONS+1)), entropy_sums)
    #plt.show()
     
def multiple_simulations():
    ##### Scenario 1: black: gradient, red: uniform
    labels = []
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'parameter': 2,
        'red': 50000,
        'black': 50000,
        'red_budget': 5000,
        'black_budget': 5000,
        'red_strat': 'uniform',
        'black_strat': 'entropy',
        'dist': 'random',
        'type': 'barabasi'
    }
    labels.append(network_initial_condition['red_strat'])
    labels.append(network_initial_condition['black_strat'])

    infection_rate_1 = run_multiple_simulations(network_initial_condition)

    ### Scenario 2:both gradient
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'parameter': 2,
        'red': 50000,
        'black': 50000,
        'red_budget': 5000,
        'black_budget': 5000,
        'red_strat': 'uniform',
        'black_strat': 'centrality_entropy',
        'dist': 'random',
        'type': 'barabasi'
    }
    labels.append(network_initial_condition['red_strat'])
    labels.append(network_initial_condition['black_strat'])
    
    infection_rate_2 = run_multiple_simulations(network_initial_condition)


    #### Scenario 3: black: uniform, red: gradient
    network_initial_condition = {
        'node_count': NODE_COUNT,
        'parameter': 2,
        'red': 50000,
        'black': 50000,
        'red_budget': 5000,
        'black_budget': 5000,
        'red_strat': 'uniform',
        'black_strat': 'centrality',
        'dist': 'random',
        'type': 'barabasi'
    }
    labels.append(network_initial_condition['red_strat'])
    labels.append(network_initial_condition['black_strat'])
    
    infection_rate_3 = run_multiple_simulations(network_initial_condition)

    plt.plot(list(range(ITERATIONS)), infection_rate_1, label = 'red: ' + labels[0] + ', black: ' + labels[1])
    plt.plot(list(range(ITERATIONS)), infection_rate_2, label = 'red: ' + labels[2] + ', black: ' + labels[3])
    plt.plot(list(range(ITERATIONS)), infection_rate_3, label = 'red: ' + labels[4] + ', black: ' + labels[5])
    plt.legend(loc='upper left')
    # plt.legend(['r: heuristic, b: gradient descent'], loc='upper left')

    plt.axis([0,ITERATIONS, 0.1, 0.9])
    plt.show()
    
def run_multiple_simulations(network_initial_condition):
    arrays_of_infection_rate = []
    for i in range(RUNS):
        print(i)
        infection_array = simulate_network_infection(network_initial_condition)
        arrays_of_infection_rate.append(infection_array)

    average_infection_rate_overtime = []
    for t in range(ITERATIONS):
        sum = 0
        for i in range(len(arrays_of_infection_rate)):
            sum += arrays_of_infection_rate[i][t]
        average = sum / len(arrays_of_infection_rate)
        average_infection_rate_overtime.append(average)

    return average_infection_rate_overtime

def simulate_network_infection(network_initial_condition):
    network = NetWorkHelper(network_initial_condition)
    G = network.create_network()
    set_positions(G)
    infection_array = []
    for node in G.node.items():
        network.construct_super_urn(node)
    for i in range(0, ITERATIONS):
        run_time_step(G, network, infection_array)
    return infection_array


def run_time_step(G, network, infection_array):
    current_conditions = {}
    network_infection_sum = 0

    network.run_time_step()
    for node in G.node.items():
        draw = draw_from_superurn(network, node)
        current_conditions[node[0]] = draw
        add_balls_to_node(G, network, node[0])
        network.construct_super_urn(node)
        network_infection_sum += node[1]['super_urn']['network_infection']
    
    network.record_entropy()
    average_infection = network_infection_sum / NODE_COUNT
    infection_array.append(average_infection)


def draw_from_superurn(network, node):
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

# Used in interactive plotting
def update_fig(G, fig, infection_array):
    pylab.clf()
    gs = fig.add_gridspec(16, 16)
    ax0 = fig.add_subplot(gs[:, :7])
    ax1 = fig.add_subplot(gs[:, 9:])
    color_map = infection_rate_to_color(G)
    nx.draw_networkx(G, nx.get_node_attributes(G, 'pos'), ax0, node_color=color_map, linewidths=1, edgecolors='black',
                     cmap=plt.cm.RdGy, alpha = 0.5, labels = nx.get_node_attributes(G, 'label'))
    
    ax1.plot(list(range(len(infection_array))), infection_array, color='green', marker='o', markersize=1)
    ax1.set_ylabel('Average Network Infection Rate')
    ax1.set_xlabel('Time')
    ax1.set_xlim([0, ITERATIONS])
    ax1.set_ylim([0.1, 0.9])
    pylab.draw()
    pause(0.001)


def set_positions(G):
    pos = nx.spring_layout(G)
    for n, p in pos.items():
        G.node[n]['pos'] = p
    for node in G.node.items():
        node[1]['label'] = node[0]


def infection_rate_to_color(G):
    color_map = []
    for node in G.node.items():
        infection_rate = node[1]['super_urn']['network_infection']
        color_map.append(1 - infection_rate)
    return color_map


if __name__ == "__main__":
    main()
