import networkx as nx
from network_helper import NetWorkHelper
import matplotlib.pyplot as plt
from graph_generator import get_graph


def main():
    # topology = 'facebook'
    # G = get_graph(topology)
    node_count = 1500
    param = 2
    G = nx.barabasi_albert_graph(node_count, param)

    strat_dict = {
        'red_budget': 100,
        'black_budget': 100,
        'red_strat': 'uniform',
        'black_strat': 'centrality',
    }

    initial_condition = {
        'node_count': node_count,
        'parameter': param,
        'red':  node_count*10,
        'black': node_count*10,
        'dist': 'random'
    }

    network = NetWorkHelper(strat_dict, G)
    G = network.create_network(initial_condition)

    degree_list = []
    for index, node in G.node.items():
        degree = G.degree(index)
        degree_list.append(degree)

    # print(degree_list)
    plt.hist(degree_list, bins=100)
    plt.xlabel('Number of edges')
    plt.ylabel('Number of nodes')
    # plt.axis([0, 150, 0, 500])
    plt.show()

if __name__ == "__main__":
        main()