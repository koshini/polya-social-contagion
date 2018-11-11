import networkx as nx
import random


class NetWorkHelper():
    def __init__(self, initial_condition):
        self.node_count = initial_condition['node_count']
        self.edges = initial_condition['edges']
        self.dist = initial_condition['dist']
        self.red = initial_condition['red']
        self.black = initial_condition['black']
        self.G = self.create_network()


    # TODO: Add distribution of red/black balls in network toggle
    def create_network(self):
        # Generate a barabasi albert graph with node_count nodes
        # Setting the second parameter to 1 means each node added will only have one edge to begin
        G = nx.barabasi_albert_graph(self.node_count, self.edges)

        # Initializes urn dictionary
        urns = {0: {'red': 1, 'black': 1}}

        # Set initial condition of urn
        # TODO: Add more distribtutions
        if self.dist == 'random':
            # Creates random distribution of starting red and black balls between all nodes
            red_dist = self.constrained_sum_sample_pos(self.red)
            black_dist = self.constrained_sum_sample_po(self.black)

        elif self.dist == 'equal':
            red_dist = self.equally_divide(self.red)
            black_dist = self.equally_divide(self.black)

        # Add distributions to urn
        for i in range(0, self.node_count):
            urns[i] = {'red': red_dist[i], 'black': black_dist[i]}

        # Adds unique urn to each node in network
        nx.set_node_attributes(G, name="urns", values=urns)
        nx.set_node_attributes(G, name="prev_draw", values=-1)
        return G


    def equally_divide(self, total):
        if self.node_count <= 0:
            return []
        else:
            dist = [total / self.node_count + 1] * (total % self.node_count) + [total / self.node_count] * \
                   (self.node_count - total % self.node_count)
            return [int(i) for i in dist]


    def constrained_sum_sample_pos(self, total):
        """Return a randomly chosen list of n positive integers summing to total.
        Each such list is equally likely to occur."""
        dividers = sorted(random.sample(range(1, total), self.node_count - 1))
        return [a - b for a, b in zip(dividers + [total], [0] + dividers)]
