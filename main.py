import networkx as nx
import random
import math
import time
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from numpy.random import choice
import pylab
from matplotlib.pyplot import pause



def main():
    pylab.ion()
    node_count = 20
    edges = 2
    initial_red = 100
    initial_black = 100
    dist = 'equal'
    added_red = 3
    added_black = 1
    
    G = create_network(node_count, edges, initial_red, initial_black, dist)
    set_positions(G)
    #print("Initial network distribution:")
    #for node in G.node.items():
            #print(node[0], "red:", node[1]['urns']['red'], "black", node[1]['urns']['black'])
    #print("\n")

    pylab.show()
    
    for i in range(0,30):
        pylab.clf()
        update_fig(G, added_red, added_black)
        pylab.draw()
        pause(1)
        

def update_fig(G, added_red, added_black):
    run_time_step(G)
    add_balls_to_nodes(G, added_red, added_black)
    color_map = set_color(G)
    nx.draw(G, nx.get_node_attributes(G,'pos'), node_color = color_map)

def set_positions(G):
    pos = nx.random_layout(G)
    for n, p in pos.items():
        G.node[n]['pos'] = p
        
def run_time_step(G, cur_time = 0):
    # Construct super urns
    current_conditions = {0 : 0}
    for node in G.node.items():
            draw = draw_from_superurn(G, node)
            current_conditions[node[0]] = draw
    #print("At time step", cur_time + 1, "the current condition is:", current_conditions, "\n")
    
    
def draw_from_superurn(G, node):
    super_urn = {'red': node[1]['urns']['red'], 'black': node[1]['urns']['black']}
    neighbors = nx.all_neighbors(G, node[0])
    for neighbor_node in neighbors:
        super_urn['red'] += G.node[neighbor_node]['urns']['red']
        super_urn['black'] += G.node[neighbor_node]['urns']['black']
    node[1]['prev_draw'] = find_condition(super_urn)
    
    return node[1]['prev_draw']
        
def add_balls_to_nodes(G, added_red, added_black):
    for node in G.node.items():
        if(node[1]['prev_draw'] == 1):
            node[1]['urns']['red'] += added_red
        elif(node[1]['prev_draw'] == 0):
            node[1]['urns']['black'] += added_black
    

def find_condition(super_urn):
    # make a list containing as many ones and zeros as there are red and black balls in the node, respectively
    red = super_urn['red']
    black = super_urn['black']
    return choice([0,1], 1, p=[black/(red+black), red/(red+black)])[0]

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def equally_divide(n, total):
    if n <= 0:
        return [] 
    else:
        dist = [total / n + 1] * (total % n) + [total / n] * (n - total % n)
        return [int(i) for i in dist]

def set_color(G):
    color_map = []
    for node in G.node.items():
        if node[1]['prev_draw'] == 1:
            color_map.append('red')
        else:
            color_map.append('black')
    return color_map
#TODO: Add distribution of red/black balls in network toggle
def create_network(node_count, edges, total_red, total_black, dist = 'random'):
    
    # Generate a barabasi albert graph with node_count nodes
    # Setting the second parameter to 1 means each node added will only have one edge to begin
    G = nx.barabasi_albert_graph(node_count, edges)
    
    #Initializes urn dictionary
    urns = { 0: {'red': 1, 'black': 1}}
    
    # Set initial condition of urns
    #TODO: Add more distribtutions
    if dist == 'random':
        #Creates random distribution of starting red and black balls between all nodes
        red_dist = constrained_sum_sample_pos(node_count, total_red)
        black_dist = constrained_sum_sample_pos(node_count, total_black)
    
    elif dist == 'equal':
        red_dist = equally_divide(node_count, total_red)
        black_dist = equally_divide(node_count, total_black)
    
    #Add distributions to urns
    for i in range(0, node_count):
        urns[i] = {'red': red_dist[i], 'black': black_dist[i]}
        
    #Adds unique urn to each node in network
    nx.set_node_attributes(G, name="urns", values=urns)
    nx.set_node_attributes(G, name="prev_draw", values=-1)
    
    return G

if __name__ == "__main__":
    main()