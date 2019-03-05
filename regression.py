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
        [model, position, centrality_ratio] = self.run_regression()
        self.model = model
        self.position = position
        self.centrality_ratio = centrality_ratio
        
    def run_regression(self):
        ## Read data
        with open('node_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            node_position = []
            node_degree = []
            node_centrality = []
            node_infection = []
            ball_dist = []
            for row in csv_reader:
                if line_count == 0:
                    node_position = list(map(int,row))
                if line_count == 1:
                    node_degree = list(map(int,row))
                if line_count == 2:
                    node_centrality = list(map(float,row))
                if line_count % 2 == 1 and line_count > 2:
                    node_infection.append(list(map(float,row)))
                if line_count % 2 ==0 and line_count > 2:
                    ball_dist.append(list(map(int,row)))
                line_count += 1
        
        
        centrality_ratio = []
        total_degree = sum(node_degree)
        total_centrality = sum(node_centrality)
        
        for i in range(0, len(node_degree)):
            centrality_ratio.append((node_degree[0]*node_centrality[0])/(total_degree*total_centrality))
        
        infection_train, infection_test, y_infection_train, y_infection_test = train_test_split( node_infection, ball_dist, test_size = 0.3, random_state = 100)
        infection = DecisionTreeClassifier(criterion = "gini", splitter = 'random', random_state = 100, max_depth = 20)
        
        
        infection.fit(infection_train, y_infection_train)
        y1_train = infection.predict(infection_train)
        y1 = infection.predict(infection_test)
        
        ## Testing
        y_pred_train = []
        for i in range(0,len(y1_train)):  
            budget = sum(y1_train[i])
            dist = np.array(centrality_ratio) * np.array(y1_train[i])
            dist = dist / sum(dist)
            dist = budget * dist
            y_pred_train.append(np.around(dist.copy()))
            
            
        y_pred = []
        for i in range(0,len(y1)):    
            budget = sum(y1[i])
            dist = np.array(centrality_ratio) * np.array(y1[i])
            dist = dist / sum(dist)
            dist = budget * dist
            y_pred.append(np.around(dist.copy()))
        
        #flat_y_pred = [item for sublist in y_pred for item in sublist]
        #flat_y1 = [item for sublist in y1 for item in sublist]
        #flat_test = [item for sublist in y_infection_test for item in sublist]
        
        #flat_y_pred_train = [item for sublist in y_pred_train for item in sublist]
        #flat_y1_train = [item for sublist in y1_train for item in sublist]
        #flat_train = [item for sublist in y_infection_train for item in sublist]
    
        return [infection, np.array(node_position), np.array(centrality_ratio)]
    
    def output_dist(self, network_infection, budget):
        network_infection = np.array(network_infection).reshape(1,-1)
        prediction = self.model.predict(network_infection)
        
        
        pred_budget = sum(prediction[0])
        dist = self.centrality_ratio * np.array(prediction[0])
        dist = dist / sum(dist)
        dist = (pred_budget * dist) * (budget/pred_budget)
        
        #where_are_NaNs = np.isnan(dist)
        #dist[where_are_NaNs] = 0

        return np.around(dist.copy())
