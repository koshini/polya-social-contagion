import networkx as nx
from main import set_positions
import pylab
import matplotlib.pyplot as plt
import pandas as pd
from network_helper import NetWorkHelper



def main():
    # G = create_graph_from_edgelist_csv('data/meetup-group-edges.csv')
    # G = create_graph_from_edgelist('data/data.edgelist')
    G = create_graph_from_matrix('data/fb-adjacency-matrix.csv')
    node_count = nx.number_of_nodes(G)
    initial_balls = node_count * 100
    budget = node_count * 10
    initial_condition = {
        'node_count': node_count,
        'edges': 2,
        'red': initial_balls,
        'black': initial_balls,
        'red_budget': budget,
        'black_budget': budget,
        'red_strat': 'uniform',
        'black_strat': 'heuristic',
        'dist': 'random',
        'type': 'barabasi',
        'heuristic_param': ['centrality', 'degree', 'infection']
    }

    network = NetWorkHelper(initial_condition)
    G = network.create_network(G=G)

    print(nx.info(G))

    # pylab.show()
    # pylab.ion()
    plt.figure(1)
    draw_graph(G)
    plt.axis('off')
    plt.suptitle('Facebook Post Network', fontsize=20)
    plt.title('Number of nodes: 30013635, Number of edges: 2425, Average degree:  3.5583', fontsize=12)
    plt.show()


    # pylab.ioff()

    # fill_out_graph()
    print()


def create_graph_from_edgelist(filename):
    # Edgelist looks like:
    # node1 node2
    # node3 node1
    # node1 node3
    # ...
    G = nx.read_edgelist(filename, create_using=nx.Graph())
    print("Read in edgelist file ", filename)
    print(nx.info(G))
    return G


# takes an adjacency matrix in csv format
def create_graph_from_matrix(filename):
    input_data = pd.read_csv(filename, header=None)
    G = nx.Graph(input_data.values)
    print(nx.info(G))
    return G


# takes an edgelist in csv format
def create_graph_from_edgelist_csv(filename):
    input_data = pd.read_csv(filename)
    G = nx.from_pandas_edgelist(input_data, create_using=nx.Graph())
    print(nx.info(G))
    return G


def draw_graph(G):
    # pylab.clf()
    pos = nx.spring_layout(G, k=1)
    color_map = set_color(G)

    nx.draw_networkx_nodes(G, pos, alpha=1, cmap=plt.cm.RdGy, linewidths=0.3, edgecolors='black',
                           node_size=[G.degree(index) for index, node in G.node.items()],
                           node_color=[infection_rate_to_color(node) for node in G.node.items()])

    nx.draw_networkx_edges(G, pos, alpha=0.05, width=0.5)


def set_color(G):
    color_map = ['red'] * len(G.node.items())
    return color_map

def infection_rate_to_color(node):
    color_map = []
    # for node in G.node.items():
    infection_rate = node[1]['super_urn']['network_infection']
    return 1-infection_rate


if __name__ == '__main__':
    main()