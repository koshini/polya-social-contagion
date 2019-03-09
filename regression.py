# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:41:11 2019

@author: ConnorK
"""

import numpy as np
from math import sqrt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error
import csv

class RegressionModel():
    def __init__(self):
        model = self.run_regression()
        self.model = model
        
    def run_regression(self):
        ## Read data
        with open('node_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            node_position = []
            node_degree = []
            node_centrality = []
            node_centrality_ratio = []
            node_infection = []
            ball_dist = []
            for row in csv_reader:
                if line_count == 0:
                    node_position = list(map(float,row))
                if line_count == 1:
                    node_degree = list(map(float,row))
                if line_count == 2:
                    node_centrality = list(map(float,row))
                if line_count % 2 == 1 and line_count > 2:
                    node_infection.append(list(map(float,row)))
                    ratio = np.multiply(np.array(node_infection[-1]), np.array(node_centrality), np.array(node_degree))
                    ratio = ratio / sum(ratio)
                    node_centrality_ratio.append(list(ratio))
                    
                if line_count % 2 ==0 and line_count > 2:
                    ball_dist.append(list(map(float,row)))
                line_count += 1
        
        centrality_dict = {}
        samples = len(node_centrality_ratio)
        nodes = len(node_centrality_ratio[0])
        
        for i in range(0, samples):
            for j in range(0, nodes):
                centrality_dict[j] = node_centrality_ratio[j]
            sorted_by_value = sorted(centrality_dict.items(), key=lambda kv: kv[1])
            node_pos = [x[0] for x in sorted_by_value]
            node_inf = [x[1] for x in sorted_by_value]
            node_infection[i] = node_inf
            
            
            new_dist = np.zeros(len(ball_dist[i]))
            for j in range(0, nodes):
                new_dist[j] = ball_dist[i][node_pos[j]]
                
        #print(sorted_by_value)    
        #print(ball_dist[i])
            
        #infection_train, infection_test, y_infection_train, y_infection_test = train_test_split( node_infection, ball_dist, test_size = 0.3, random_state = 100)
        #infection = DecisionTreeClassifier(criterion = "gini", splitter = 'random', random_state = 100, max_depth = 20)
        
        centrality_train, centrality_test, y_centrality_train, y_centrality_test = train_test_split( node_centrality_ratio, ball_dist, test_size = 0.3, random_state = 100)
        centrality = DecisionTreeClassifier(criterion = "gini", splitter = 'random', random_state = 100)
        
        #infection.fit(infection_train, y_infection_train)
        #y1_train = infection.predict(infection_train)
        #y1 = infection.predict(infection_test)
        
        centrality.fit(centrality_train, y_centrality_train)
        y1_train = centrality.predict(centrality_train)
        y1 = centrality.predict(centrality_test)
        
        
        #flat_y_pred = [item for sublist in y_pred for item in sublist]
        #flat_y1 = [item for sublist in y1 for item in sublist]
        #flat_test = [item for sublist in y_infection_test for item in sublist]
        
        #flat_y_pred_train = [item for sublist in y_pred_train for item in sublist]
        #flat_y1_train = [item for sublist in y1_train for item in sublist]
        #flat_train = [item for sublist in y_infection_train for item in sublist]
    
        return centrality
    
    def output_dist(self, network_infection, centrality_array, budget):
        #network_infection = np.array(network_infection).reshape(1,-1)
        centrality = centrality_array * np.array(network_infection[0])
        centrality = centrality / sum(centrality)
        
        centrality_dict = {}
        for j in range(0, len(network_infection)):
            centrality_dict[j] = centrality[j]
        sorted_by_value = sorted(centrality_dict.items(), key=lambda kv: kv[1])
        node_pos = [x[0] for x in sorted_by_value]
        node_inf = [x[1] for x in sorted_by_value]
        centrality = node_inf
        
        centrality = np.array(centrality).reshape(1,-1)
        prediction = self.model.predict(centrality)[0]
        pred_budget = sum(prediction)
        
        dist = np.zeros(len(node_pos))
        
        for i in range(0, len(node_pos)):
            dist[node_pos[i]] = prediction[i]
            
        dist = prediction * (budget/pred_budget)
        
        #where_are_NaNs = np.isnan(dist)
        #dist[where_are_NaNs] = 0

        return np.around(dist.copy())
