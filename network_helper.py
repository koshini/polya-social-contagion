import networkx as nx
import json
import random
import numpy as np
import operator as op
import math
import operator


class NetWorkHelper():
    def __init__(self, strat_dict, G, targets=None):
        self.node_count = nx.number_of_nodes(G)
        self.red_budget = strat_dict['red_budget']
        self.black_budget = strat_dict['black_budget']
        self.red_dist = self.node_count * [0]
        self.black_dist = self.node_count * [0]
        self.red_strat = strat_dict['red_strat']
        self.black_strat = strat_dict['black_strat']
        self.strat_dict = strat_dict
        self.G = G
        self.targets = targets

    # TODO: Add distribution of red/black balls in network toggle
    def create_network(self, initial_condition):
        G = self.G
        # Initializes urn dictionary
        urns = {}
        prev_exposure = []

        # Set initial condition of urn
        # TODO: Add more distribtutions
        if initial_condition['dist'] == 'random':
            # Creates random distribution of starting red and black balls between all nodes
            red_dist = self.more_random_initial_dist(initial_condition['red'])
            black_dist = self.more_random_initial_dist(initial_condition['black'])

        elif initial_condition['dist'] == 'equal':
            red_dist = self.equally_divide(initial_condition['red'])
            black_dist = self.equally_divide(initial_condition['black'])

        # Add distributions to urn
        for key in G.nodes.keys():
            urns[key] = {'red': red_dist[key], 'black': black_dist[key]}


        # Adds unique urn to each node in network
        nx.set_node_attributes(G, name="urns", values=urns)
        nx.set_node_attributes(G, name="prev_draw", values=-1)
        nx.set_node_attributes(G, name="prev_exposure", values=prev_exposure) # not being used
        # nx.set_node_attributes(G, name="prev_deltar", values=0)
        # nx.set_node_attributes(G, name="prev_deltab", values=0)
        nx.set_node_attributes(G, name="entropy", values=[])
        
        # #Set the intitial budget distributions
        # G.node[0]['prev_deltar'] = self.red_budget
        # G.node[0]['prev_deltab'] = self.black_budget

        # self.black_dist = self.equally_divide(self.black_budget)
        # self.red_dist = self.equally_divide(self.red_budget)
        
        #Set initial exposure rate
        self.G = G
        self.set_prev_exposure()

        # construct superurn
        for node in G.node.items():
            self.construct_super_urn(node)

        return self.G

    def run_time_step(self):
        if self.black_strat == 'uniform':
            curing_dist = self.equally_divide(self.black_budget)
        if self.black_strat == 'random':
            curing_dist = self.constrained_sample_sum_pos(self.black_budget)            
        if self.black_strat == 'gradient':
            curing_dist = self.black_gradient_descent()
        if self.black_strat == 'centrality_ratio':
            curing_dist = self.black_centrality_ratio_strat()
        if self.black_strat == 'regression':
            curing_dist = self.run_regression()
        if self.black_strat == 'follow_bot':
            curing_dist = self.follow_bot()
        if self.black_strat == 'threshold':
            curing_dist = self.threshold()
        if self.black_strat == 'centrality_threshold':
            curing_dist = self.centrality_threshold()
        if self.black_strat == 'pure_centrality_threshold':
            curing_dist = self.pure_centrality_threshold()
        if self.black_strat == 'pure_centrality':
            curing_dist = self.pure_centrality()
        if self.black_strat == 'entropy':
            curing_dist = self.entropy()
        if self.black_strat == 'entropy2':
            curing_dist = self.entropy2()
        if self.black_strat == 'entropy3':
            curing_dist = self.entropy3()
        if self.entropy() == 'entropy_ratio':
            curing_dist = self.entropy_ratio()
        if self.black_strat == 'bot':
            curing_dist = self.bot_strat_black()
        if self.black_strat == 'pure_closeness':
            curing_dist = self.pure_closeness()
        if self.black_strat == 'pure_degree':
            curing_dist = self.pure_degree()
        if self.black_strat == 'pure_exposure':
            curing_dist = self.pure_exposure()


        if self.red_strat == 'uniform':
            infecting_dist = self.equally_divide(self.red_budget)
        if self.red_strat == 'random':
            infecting_dist = self.constrained_sample_sum_pos(self.red_budget)
        if self.red_strat == 'gradient':
            infecting_dist = self.red_gradient_descent()
        if self.red_strat == 'centrality_ratio':
            infecting_dist = self.red_centrality_ratio_strat()
        if self.red_strat == 'bot':
            infecting_dist = self.bot_strat()
            
        self.set_distributions(curing_dist, infecting_dist)

            
    def equally_divide(self, total):
        if self.node_count <= 0:
            return []
        else:
            dist = [total / self.node_count + 1] * (total % self.node_count) + [total / self.node_count] * \
                   (self.node_count - total % self.node_count)
            return [int(i) for i in dist]


    def constrained_sample_sum_pos(self, total):
        """Return a randomly chosen list of n positive integers summing to total.
        Each such list is equally likely to occur."""
        dividers = sorted(random.sample(range(1, total), self.node_count - 1))
        random_dist = [a - b for a, b in zip(dividers + [total], [0] + dividers)]
        return random_dist

    def more_random_initial_dist(self, total):
        dist = self.constrained_sample_sum_pos(total)
        # randomly pick 20% of total nodes and add 50% balls
        choices = random.choices(dist, k = int(self.node_count / 5))
        for i in range(len(dist)):
            if i in choices:
                dist[i] += 50
        return dist

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
        node[1]['network_infection'] = network_infection
        node[1]['super_urn'] = super_urn
        return super_urn
    
    def record_entropy(self):
        for index, node in self.G.node.items():
            p = 1 - node['network_infection']
            #node['entropy'].append(-p*math.log(p))
            node['entropy'].append(-p*math.log(p)-(1-p)*math.log(1-p))

    def record_wasted_budget(self, node, waste):
        node['wasted_budget'] = waste
        
    def find_superurn_exp_red(self, infecting_strat = None):
        if infecting_strat == None:
            infecting_strat = self.red_dist

        exp_red = {}
        for node in self.G.node.items():
            exp_red_temp = 0 
            exp_red_temp += node[1]['super_urn']['network_infection']*infecting_strat[node[0]]
            neighbors = nx.all_neighbors(self.G, node[0])
            for nd in neighbors:
                exp_red_temp += self.G.node[nd]['super_urn']['network_infection']*infecting_strat[nd]
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
    

    def calc_node_partial_exposure_black(self, node, exp_red, exp_black):
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
        
    def calc_node_partial_exposure_red(self, node, exp_red, exp_black):
        node_exp = node[1]['super_urn']['network_infection']
        neighbors = nx.all_neighbors(self.G, node[0])
        all_nodes = []
        all_nodes.append(node[0])
        partial_exp_sum = 0
        for x in neighbors:
            all_nodes.append(x)
        for nd in all_nodes:
            numerator = -(self.G.node[nd]['super_urn']['black'] + exp_black[nd])*(node_exp)
            denominator = (self.G.node[nd]['super_urn']['black'] + self.G.node[nd]['super_urn']['red'] + exp_red[nd] + exp_black[nd])**2
            partial_exp_sum += (numerator/denominator)
        return partial_exp_sum
    
    #Also doesnt always output full budget worth of distribution
    def black_gradient_descent(self):
        #This stays constant at every step of the gradient descent right now
        #due to us only changing our curing strategy
        exp_red = self.find_superurn_exp_red()
        step = 0.1
        curing_dist = self.node_count * [0]
        curing_dist[0] = self.black_budget
        
        for k in range(0,100):
            next_partial_exposures = []
            next_strat = []
            for node in self.G.node.items():
                next_strat.append(0)
                
            exp_black = self.find_superurn_exp_black(curing_dist)
            for node in self.G.node.items():
                next_partial_exposures.append(self.calc_node_partial_exposure_black(node, exp_red, exp_black))
            min_index = next_partial_exposures.index(min(next_partial_exposures))
            next_strat[min_index] = self.black_budget
            temp_array = list( map(op.sub, next_strat, curing_dist) )
            temp_array = [x*step for x in temp_array]
            curing_dist = list( map(op.add, curing_dist, temp_array) )
        for index,x in enumerate(curing_dist):
            curing_dist[index] = round(x)
        return curing_dist
    
    def red_gradient_descent(self):
        #This stays constant at every step of the gradient descent right now
        #due to us only changing our curing strategy
        exp_black = self.find_superurn_exp_black()
        step = 0.1
        infecting_dist = self.node_count * [0]
        infecting_dist[0] = self.red_budget
        
        for k in range(0,100):
            next_partial_exposures = []
            next_strat = []
            for node in self.G.node.items():
                next_strat.append(0)
                
            exp_red = self.find_superurn_exp_red(infecting_dist)
            for node in self.G.node.items():
                next_partial_exposures.append(self.calc_node_partial_exposure_red(node, exp_red, exp_black))
            min_index = next_partial_exposures.index(min(next_partial_exposures))
            next_strat[min_index] = self.red_budget
            temp_array = list( map(op.sub, next_strat, infecting_dist) )
            temp_array = [x*step for x in temp_array]
            infecting_dist = list( map(op.add, infecting_dist, temp_array) )
        for index,x in enumerate(infecting_dist):
            infecting_dist[index] = round(x)
        return infecting_dist

    def get_centrality_infection(self):
        # closeness centrality
        closeness_centrality_dict = nx.closeness_centrality(self.G)

        centrality_infection_sum = 0
        for index, node in self.G.node.items():
            degree = self.G.degree(index)
            closeness_centrality = closeness_centrality_dict[index]
            infection_rate = node['super_urn']['network_infection']
            ##### parameters: degree, closeness, infection
            centrality_infection = degree*closeness_centrality*infection_rate
            node['centrality_infection'] = centrality_infection
            centrality_infection_sum += centrality_infection
        return centrality_infection_sum

    #TODO: Fix this: This does not always output a distribution that adds to budget.
    #We should probably also run the entire strat with one call and not give it node by node
    def black_centrality_ratio_strat(self):
        infection_array = np.array(list(nx.get_node_attributes(self.G,'network_infection').values()))
        centrality_mult_array = np.array(list(nx.get_node_attributes(self.G,'centrality_multiplier').values()))
        curing_dist = np.multiply(infection_array, centrality_mult_array)
        # curing_dist = centrality_mult_array
        curing_dist = curing_dist / sum(curing_dist)
        curing_dist = np.around(curing_dist * self.black_budget)        
        return list(curing_dist)

    def red_centrality_ratio_strat(self):
        infection_array = 1 - np.array(list(nx.get_node_attributes(self.G,'network_infection').values()))
        centrality_mult_array = np.array(list(nx.get_node_attributes(self.G,'centrality_multiplier').values()))
        infecting_dist = np.multiply(infection_array, centrality_mult_array)
        infecting_dist = infecting_dist / sum(infecting_dist)
        infecting_dist = np.around(infecting_dist * self.red_budget)        
        return list(infecting_dist)

    
    def set_centrality_mult(self, filepath=None):
        if not filepath:
            closeness_centrality_dict = nx.closeness_centrality(self.G)
        else: # closeness_centrality_dict is previously computed and stored in a JSON file
            f = open(filepath, 'r').read()
            closeness_centrality_dict = json.loads(f)

        for index, node in self.G.node.items():
            degree = self.G.degree(index)
            # closeness_centrality = closeness_centrality_dict[index]
            closeness_centrality = closeness_centrality_dict[str(index)] # use this for twitter and meetup
            centrality_mult = degree*closeness_centrality
            node['centrality_multiplier'] = centrality_mult
            node['closeness'] = closeness_centrality
            node['degree'] = degree

        
    def set_distributions(self, curing_dist, infecting_dist):
        self.black_dist = curing_dist
        self.red_dist = infecting_dist
        
    def run_regression(self):
        infection_array = []
        centrality_array = []
        for index, node in self.G.node.items():
            infection_array.append(node['super_urn']['network_infection'])
            centrality_array.append(node['centrality_multiplier'])
        curing_dist = list(self.regression_model.output_dist(infection_array, centrality_array, self.black_budget))
        return curing_dist
    
    def follow_bot(self):
        curing_dist = np.array(self.red_dist)
        curing_dist = curing_dist * (self.black_budget / self.red_budget)
        return curing_dist
        
    def threshold(self):
        infection_array = np.array(list(nx.get_node_attributes(self.G,'network_infection').values()))
        
        for i in range(0, len(infection_array)):
            if infection_array[i] < 0.5:
                infection_array[i] = 0
        #If all nodes less than 50%% infected uniformly distribute budget
        if(sum(infection_array) == 0):
            return self.equally_divide(self.black_budget)
        
        infection_array = infection_array / sum(infection_array)
        dist = list(np.around(infection_array * (self.black_budget)))

        return dist  
    
    def centrality_threshold(self):
            infection_array = np.array(list(nx.get_node_attributes(self.G,'network_infection').values()))
            adj_infection_array = infection_array
            centrality_mult_array = np.array(list(nx.get_node_attributes(self.G,'centrality_multiplier').values()))

            for i in range(0, len(adj_infection_array)):
                if adj_infection_array[i] < self.strat_dict['threshold']:
                    adj_infection_array[i] = self.strat_dict['portion']
            if(sum(adj_infection_array) == 0):
                return self.equally_divide(self.black_budget)  
                
            adj_infection_array = np.multiply(adj_infection_array, centrality_mult_array) / sum(np.multiply(adj_infection_array,centrality_mult_array))
            dist = list(np.around(adj_infection_array * (self.black_budget)))
    
            return dist
    
    def pure_centrality_threshold(self):
            infection_array = np.array(list(nx.get_node_attributes(self.G,'network_infection').values()))
            adj_infection_array = infection_array
            centrality_mult_array = np.array(list(nx.get_node_attributes(self.G,'centrality_multiplier').values()))

            for i in range(0, len(adj_infection_array)):
                if adj_infection_array[i] < 0.4:
                    adj_infection_array[i] = 0
            #If all nodes less than 60% infected uniformly distribute budget                    
            if(sum(adj_infection_array) == 0):
                return self.equally_divide(self.black_budget)  
                
            adj_infection_array = np.multiply(adj_infection_array, centrality_mult_array) / sum(np.multiply(adj_infection_array,centrality_mult_array))
            dist = list(np.around(adj_infection_array * (self.black_budget)))
    
            return dist
    
    def bot_strat(self):
            infection_array = np.array(list(nx.get_node_attributes(self.G,'network_infection').values()))
            adj_infection_array = np.absolute(infection_array - 0.5)
            adj_infection_array = np.multiply(adj_infection_array, adj_infection_array)
            centrality_mult_array = np.array(list(nx.get_node_attributes(self.G,'centrality_multiplier').values()))
                
            adj_infection_array = np.multiply(adj_infection_array, centrality_mult_array) / sum(np.multiply(adj_infection_array,centrality_mult_array))
            dist = list(np.around(adj_infection_array * (self.red_budget)))
    
            return dist

    def bot_strat_black(self):
        infection_array = np.array(list(nx.get_node_attributes(self.G, 'network_infection').values()))
        adj_infection_array = np.absolute(infection_array - 0.5)
        adj_infection_array = np.multiply(adj_infection_array, adj_infection_array)
        centrality_mult_array = np.array(list(nx.get_node_attributes(self.G, 'centrality_multiplier').values()))

        adj_infection_array = np.multiply(adj_infection_array, centrality_mult_array) / sum(
            np.multiply(adj_infection_array, centrality_mult_array))
        dist = list(np.around(adj_infection_array * (self.black_budget)))

        return dist

    def set_centrality_ranking(self):
        list = sorted(nx.get_node_attributes(self.G, 'centrality_multiplier').items(), key=operator.itemgetter(1), reverse=True)
        for i in range(len(list)):
            self.G.node[list[i][0]]['centrality_rank'] = i


    def pure_centrality(self):
        centrality_mult_array = np.array(list(nx.get_node_attributes(self.G,'centrality_multiplier').values()))
        curing_dist = centrality_mult_array / sum(centrality_mult_array)
        curing_dist = np.around(curing_dist * self.black_budget)
        return list(curing_dist)


    def pure_exposure(self):
        infection_array = np.array(list(nx.get_node_attributes(self.G, 'network_infection').values()))
        curing_dist = infection_array / sum(infection_array)
        curing_dist = np.around(curing_dist * self.black_budget)
        return list(curing_dist)

    def pure_degree(self):
        degree_array = np.array(list(nx.get_node_attributes(self.G,'degree').values()))
        curing_dist = degree_array / sum(degree_array)
        curing_dist = np.around(curing_dist * self.black_budget)
        return list(curing_dist)

    def pure_closeness(self):
        closeness_array = np.array(list(nx.get_node_attributes(self.G,'closeness').values()))
        curing_dist = closeness_array / sum(closeness_array)
        curing_dist = np.around(curing_dist * self.black_budget)
        return list(curing_dist)


    # Given a list of target node indeces, further target ones with high exposure
    def entropy2(self):
        refined_target = []
        for index, node in self.G.node.items():
            if index in self.targets:
                if node['super_urn']['network_infection'] > 0.6:
                    refined_target.append(index)
        if len(refined_target) == 0:
            dist = self.black_centrality_ratio_strat()
        else:
            large_budget = int(self.black_budget / len(self.targets))
            extra_budget = self.black_budget - (large_budget * len(refined_target))
            small_budget = round(extra_budget / (self.node_count - len(refined_target)))
            dist = [small_budget] * self.node_count
            for i in range(len(dist)):
                if i in refined_target:
                    dist[i] = round(large_budget)
        return dist

    def entropy(self):
        infection_array = np.array(list(nx.get_node_attributes(self.G, 'network_infection').values()))
        adj_infection_array = np.array(infection_array - 0.5)
        for i, x in enumerate(adj_infection_array):
            adj_infection_array[i] = x * x if (x>0) else 0

        if (sum(adj_infection_array) == 0):
            return self.pure_centrality()

        adj_infection_array = adj_infection_array / sum (adj_infection_array)
        dist = list(np.around(adj_infection_array * (self.black_budget)))

        return dist

    # Target the ones that's on our side
    def entropy3(self):
        infection_array = np.array(list(nx.get_node_attributes(self.G, 'network_infection').values()))
        adj_infection_array = np.array((1-infection_array) - 0.5)
        for i, x in enumerate(adj_infection_array):
            adj_infection_array[i] = x * x if (x>0) else 0

        if (sum(adj_infection_array) == 0):
            return self.pure_centrality()

        adj_infection_array = adj_infection_array / sum (adj_infection_array)
        dist = list(np.around(adj_infection_array * (self.black_budget)))

        return dist

    def entropy_ratio(self):
        infection_array = np.array(list(nx.get_node_attributes(self.G, 'network_infection').values()))

        infection_array = infection_array / sum (infection_array)
        dist = list(np.around(infection_array * (self.black_budget)))

        return dist






