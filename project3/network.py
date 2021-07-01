# -*- coding: UTF-8 -*-
# Author: Junbin Zhang
# E-mail: p78083025@ncku.edu.tw
# Update time: 2021.02.27

from __future__ import print_function

class NETWORK():
    def __init__(self):
        self.network = {}
        self.table = {}
        self.shortest_path = []
        
        for i in range(12):
            self.table[i] = 99
            self.shortest_path.append([])

    def Creat_network(self, network):
        self.network = network
        return self.network

    def Get_network(self, network):
        '''
        self.network = {'r0': [1,3],'r1': [0,2,3],'r2': [1,5],'r3': [0,1,4],'r4': [3,5,6],'r5': [2,4,7],'r6': [4,7,10],
             'r7': [5,6,8,9],'r8': [7],'r9': [7,11],'r10': [6,11],'r11': [9,10]}
        '''
        self.network = network
        return self.network

    def Bulid_network_graph(self, route_ID, network):
        self.table[route_ID] = 0
        for i in network["r" + str(route_ID)]:
            self.table[i] = 1
            self.shortest_path[i] = []
            path = []
            path.append(i)
            self.shortest_path[i].append(i)
            self.DFS(i, 2, network, path)

        return self.table, self.shortest_path

    def DFS(self, i, n, network, path):
        for j in network["r" + str(i)]:
            tmp = []
            for i in range(len(path)):
                tmp.append(path[i])
            if n < self.table[j]:
                self.table[j] = n
                self.shortest_path[j] = []
                tmp.append(j)
                for i in range(len(tmp)):
                    self.shortest_path[j].append(tmp[i])
                
                self.DFS(j, n + 1, network, tmp)
