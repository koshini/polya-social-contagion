import networkx as nx
import random
import copy
import operator as op
import math


class NetWorkHelper():
    def __init__(self, initial_condition):
        self.node_count = initial_condition['node_count']
        self.edges = initial_condition['edges']
        self.dist = initial_condition['dist']
        self.red = initial_condition['red']
        self.black = initial_condition['black']
        self.red_budget = initial_condition['red_budget']
        self.black_budget = initial_condition['black_budget']
        self.red_dist = self.node_count * [0]
        self.black_dist = self.node_count * [0]
        self.red_strat = initial_condition['red_strat']
        self.black_strat = initial_condition['black_strat']
        self.type = initial_condition['type']
        self.heuristic_param = initial_condition['heuristic_param']
        self.G = None

    # TODO: Add distribution of red/black balls in network toggle
    def create_network(self, G=None):
        # if no graph is provided, we simulate one
        #####
        # G=None
        if not G:
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
            black_dist = self.constrained_sum_sample_pos(self.black)

        elif self.dist == 'equal':
            red_dist = self.equally_divide(self.red)
            black_dist = self.equally_divide(self.black)

        # Add distributions to urn
        i = 0
        for key in G.nodes.keys():
            urns[key] = {'red': red_dist[i], 'black': black_dist[i]}
            i += 1

        # Adds unique urn to each node in network
        nx.set_node_attributes(G, name="urns", values=urns)
        nx.set_node_attributes(G, name="prev_draw", values=-1)
        nx.set_node_attributes(G, name="prev_exposure", values=prev_exposure) # not being used
        nx.set_node_attributes(G, name="prev_deltar", values=0)
        nx.set_node_attributes(G, name="prev_deltab", values=0)
        
        #Set the intitial budget distributions
        # G.node[0]['prev_deltar'] = self.red_budget
        # G.node[0]['prev_deltab'] = self.black_budget
        
        #Set initial exposure rate
        self.G = G
        self.set_prev_exposure()


        # construct superurn
        for node in G.node.items():
            self.construct_super_urn(node)

        return self.G

    def run_time_step(self):
        if self.black_strat == 'uniform':
            self.black_dist = self.equally_divide(self.black_budget)
        if self.black_strat == 'random':
            self.black_dist = self.constrained_sample_sum_pos(self.black_budget)            
        if self.black_strat == 'gradient':
            self.black_gradient_descent()
        if self.black_strat == 'heuristic':
            self.black_heuristic_strat()


        
        # print('Black dist:', self.black_dist)

        if self.red_strat == 'uniform':
            self.red_dist = self.equally_divide(self.red_budget)
        if self.red_strat == 'random':
            self.red_dist = self.constrained_sample_sum_pos(self.red_budget)
        if self.red_strat == 'gradient':
            self.red_gradient_descent()
        if self.red_strat == 'heuristic':
            self.red_heuristic_strat()

        # print('Red dist:', self.red_dist)

        

        
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

    # Not being used
    def set_prev_exposure(self):
        for node in self.G.node.items():
            total_red = 0
            total_balls = 0
            
            total_red += node[1]['urns']['red']
            total_balls += node[1]['urns']['red'] + node[1]['urns']['black']
            
            neighbors = nx.all_neighbors(self.G, node[0])
            for neighbor_node in neighbors:
                total_red += self.G.node[neighbor_node]['urns']['red']
                total_balls += self.G.node[neighbor_node]['urns']['red'] + self.G.node[neighbor_node]['urns']['black']
            
            node[1]['prev_exposure'] = total_red/total_balls
    
    def construct_super_urn(self, node):
        # Construct super urns
        super_urn = {'red': node[1]['urns']['red'], 'black': node[1]['urns']['black']}
        neighbors = nx.all_neighbors(self.G, node[0])
        for neighbor_node in neighbors:
            super_urn['red'] += self.G.node[neighbor_node]['urns']['red']
            super_urn['black'] += self.G.node[neighbor_node]['urns']['black']
    
        # network_infection(Si,n) = proportion of the red balls in the node's super urn
        network_infection = super_urn['red'] / (super_urn['red'] + super_urn['black'])
        super_urn['network_infection'] = network_infection
        node[1]['super_urn'] = super_urn
        return super_urn
    
    def find_superurn_exp_red(self, infecting_strat = None):
        if infecting_strat == None:
            infecting_strat = self.red_dist

        exp_red = {}
        for node in self.G.node.items():
            exp_red_temp = 0 
            exp_red_temp += node[1]['super_urn']['network_infection']*self.red_dist[node[0]]
            neighbors = nx.all_neighbors(self.G, node[0])
            for nd in neighbors:
                exp_red_temp += self.G.node[nd]['super_urn']['network_infection']*self.red_dist[nd]
            exp_red[node[0]] = exp_red_temp
        return exp_red
            
    def find_superurn_exp_black(self, curing_strat = None):
        if curing_strat == None:
            curing_strat = self.black_dist
            
        exp_black = {}
        for node in self.G.node.items():
            exp_black_temp = 0 
            exp_black_temp += (1 - node[1]['super_urn']['network_infection'])*curing_strat[node[0]]
            neighbors = nx.all_neighbors(self.G, node[0])
            for nd in neighbors:
                exp_black_temp += (1 - self.G.node[nd]['super_urn']['network_infection'])*curing_strat[nd]
            exp_black[node[0]] = exp_black_temp
        return exp_black
    

    def calc_node_partial_exposure(self, node, exp_red, exp_black):
        node_exp = node[1]['super_urn']['network_infection']
        neighbors = nx.all_neighbors(self.G, node[0])
        all_nodes = []
        all_nodes.append(node[0])
        partial_exp_sum = 0
        for x in neighbors:
            all_nodes.append(x)
        for nd in all_nodes:
            numerator = -(self.G.node[nd]['super_urn']['red'] + exp_red[nd])*(1-node_exp)
            denominator = (self.G.node[nd]['super_urn']['black'] + self.G.node[nd]['super_urn']['red'] + exp_red[nd] + exp_black[nd])**2
            partial_exp_sum += (numerator/denominator)
        return partial_exp_sum
        
    #Also doesnt always output full budget worth of distribution
    def black_gradient_descent(self):
        #This stays constant at every step of the gradient descent right now
        #due to us only changing our curing strategy
        exp_red = self.find_superurn_exp_red()
        step = 0.1
        curing_strat = self.node_count * [0]
        infecting_strat = self.node_count * [0]

        curing_strat[0] = self.black_budget
        infecting_strat[0] = self.red_budget
        
        for k in range(0,100):
            next_partial_exposures = []
            next_strat = []
            for node in self.G.node.items():
                next_strat.append(0)
                
            exp_black = self.find_superurn_exp_black(curing_strat)
            for node in self.G.node.items():
                next_partial_exposures.append(self.calc_node_partial_exposure(node, exp_red, exp_black))
            min_index = next_partial_exposures.index(min(next_partial_exposures))
            next_strat[min_index] = self.black_budget
            temp_array = list( map(op.sub, next_strat, curing_strat) )
            temp_array = [x*step for x in temp_array]
            curing_strat = list( map(op.add, curing_strat, temp_array) )
        for index,x in enumerate(curing_strat):
            curing_strat[index] = round(x)
        self.black_dist = curing_strat
    
    def red_gradient_descent(self):
        #This stays constant at every step of the gradient descent right now
        #due to us only changing our curing strategy
        exp_black = self.find_superurn_exp_black()
        step = 0.1
        curing_strat = self.node_count * [0]
        infecting_strat = self.node_count * [0]

        curing_strat[0] = self.black_budget
        infecting_strat[0] = self.red_budget
        
        for k in range(0,100):
            next_partial_exposures = []
            next_strat = []
            for node in self.G.node.items():
                next_strat.append(0)
                
            exp_red = self.find_superurn_exp_black(infecting_strat)
            for node in self.G.node.items():
                next_partial_exposures.append(self.calc_node_partial_exposure(node, exp_red, exp_black))
            min_index = next_partial_exposures.index(min(next_partial_exposures))
            next_strat[min_index] = self.red_budget
            temp_array = list( map(op.sub, next_strat, infecting_strat) )
            temp_array = [x*step for x in temp_array]
            infecting_strat = list( map(op.add, infecting_strat, temp_array) )
        for index,x in enumerate(infecting_strat):
            infecting_strat[index] = round(x)
        self.red_dist = infecting_strat

    def get_heuristic_parameters(self):
        closeness_centrality_dict = nx.closeness_centrality(self.G)
        parameter_sum = 0

        for index, node in self.G.node.items():
            if 'degree' in self.heuristic_param:
                degree = self.G.degree(index)
            else:
                degree = 1

            if 'centrality' in self.heuristic_param:
                centrality = closeness_centrality_dict[index]
            else:
                centrality = 1

            if 'infection' in self.heuristic_param:
                infection = node['super_urn']['network_infection']

            else:
                infection = 1
            ##### parameters: degree, closeness, infection
            heuristic_parameters = degree*centrality*infection
            node['heuristic_parameters'] = heuristic_parameters
            parameter_sum += heuristic_parameters
        return parameter_sum

    #TODO: Fix this: This does not always output a distribution that adds to budget.
    #We should probably also run the entire strat with one call and not give it node by node
    def black_heuristic_strat(self):
        for node in self.G.node.items():
            parameter_sum = self.get_heuristic_parameters()
            ratio = node[1]['heuristic_parameters'] / parameter_sum
            balls = round(self.black_budget * ratio)
            self.black_dist[node[0]] = balls
        return balls

    def red_heuristic_strat(self):
        for node in self.G.node.items():
            parameter_sum = self.get_heuristic_parameters()
            ratio = node[1]['heuristic_parameters'] / parameter_sum
            balls = round(self.red_budget * ratio)
            self.red_dist[node[0]] = balls
        return balls


        
        