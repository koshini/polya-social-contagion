import networkx as nx
import random
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


def main():
    # G = nx.Graph()
    # Generate a barabasi albert graph with 5 nodes each with 1 edge
    G = nx.barabasi_albert_graph(5, 1)

    # Initial condition - start with 5 red and 5 black balls in each urn
    balls = {
        0: {'red': 5, 'black': 5},
        1: {'red': 5, 'black': 5},
        2: {'red': 5, 'black': 5},
        3: {'red': 5, 'black': 5},
        4: {'red': 5, 'black': 5}
    }
    nx.set_node_attributes(G, name="balls", values=balls)

    ##### Draw from each urn for 10 times, and add n red balls if red is drawn #####
    n = 3
    super_urns = {}
    for t in range(10):
        print("-------------- at time: " + str(t) + " --------------")
        additional_red_balls = []
        ##### Draw from each node #####
        for key, value in G.node.items():
            red = draw_from_node(value)
            # if it is 1(i.e it is red) add n red balls to the urn, if it's black do nothing
            if red:
                print("red drawn")
                additional_red_balls.append(n)
            else:
                additional_red_balls.append(0)

            ##### TODO: draw from super urn #####
            # Construct super urns
            neighbors = nx.all_neighbors(G, key)
            super_urn = []
            for node in neighbors:
                super_urn.append(node)
            # Store the super urn for this node in a dictionary
            super_urns[key] = {'neighbours': super_urn}

        # add red balls to nodes
        add_red_balls_to_nodes(balls, additional_red_balls)
        print(balls)

    nx.draw(G)
    plt.show()
    # adj_dict = nx.to_dict_of_dicts(G)



def add_red_balls_to_nodes(current_condition, red_list):
    for key, value in current_condition.items():
        value['red'] += red_list[key]


def draw_from_node(node):
    # make a list containing as many ones and zeros as there are red and black balls in the node, respectively
    red = [1] * node['balls']['red']
    black = [0] * node['balls']['black']
    joined = red + black
    # shuffle the list and pick the first one
    random.shuffle(joined)
    return joined[0]


if __name__ == "__main__":
    main()