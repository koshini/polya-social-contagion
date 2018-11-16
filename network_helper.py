import networkx as nx
import random


class NetWorkHelper():
    def __init__(self, initial_condition):
        self.node_count = initial_condition['node_count']
        self.edges = initial_condition['edges']
        self.dist = initial_condition['dist']
        self.red = initial_condition['red']
        self.black = initial_condition['black']
        self.red_budget = initial_condition['red_budget']
        self.black_budget = initial_condition['black_budget']
        self.type = initial_condition['type']
        self.G = self.create_network()


    # TODO: Add distribution of red/black balls in network toggle
    def create_network(self):
        # Generate a barabasi albert graph with node_count nodes
        # Setting the second parameter to 1 means each node added will only have one edge to begin
        if self.type == 'barabasi':
            G = nx.barabasi_albert_graph(self.node_count, self.edges)
        elif self.type == 'path':
            G = nx.path_graph(self.node_count)
        # Initializes urn dictionary
        urns = {}
        prev_exposure = []

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
        nx.set_node_attributes(G, name="prev_exposure", values=prev_exposure)
        nx.set_node_attributes(G, name="prev_deltar", values=0)
        nx.set_node_attributes(G, name="prev_deltab", values=0)
        
        #Set the intitial budget distributions
        G.node[0]['prev_deltar'] = self.red_budget
        G.node[0]['prev_deltab'] = self.black_budget
        
        #Set initial exposure rate
        self.set_prev_exposure(G)
        
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

    def set_prev_exposure(self, G):
        
        for node in G.node.items():
            total_red = 0
            total_balls = 0
            
            total_red += node[1]['urns']['red']
            total_balls += node[1]['urns']['red'] + node[1]['urns']['black']
            
            neighbors = nx.all_neighbors(G, node[0])
            for neighbor_node in neighbors:
                total_red += G.node[neighbor_node]['urns']['red']
                total_balls += G.node[neighbor_node]['urns']['red'] + G.node[neighbor_node]['urns']['black']
            
            node[1]['prev_exposure'] = total_red/total_balls