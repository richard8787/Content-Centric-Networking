# -*- coding: UTF-8 -*-
# Author: Junbin Zhang
# E-mail: p78083025@ncku.edu.tw
# Update time: 2021.03.21

from __future__ import print_function
import time
import random

class CS():
    def __init__(self):
        self.cs = []
        self.cs_entry = []

        # Each router creates an independent cache space

    def Creat_cs(self, route_ID):
        '''
        cs = [[content_name, data, time, cost],
              ...
             ]
        '''
        return self.cs

        # Get cs

    def Get_cs(self, route_ID):
        return self.cs

        # Check if there is data matching the content name in cs

    def Search_cs_interest(self, cs, content_name):
        '''
        cs = [[content_name, data, time, cost],...]
        cs_entry = [content_name, data, time, cost]
        '''
        # self.cs = cs

        for cs_entry in cs:
            if content_name == cs_entry[0]:
                cs[cs.index(cs_entry)][1] += 1 
                # cs_entry[-1] += 1
                return True
        # No data for content name found in cs
        return False

        # Add an entry to CS

    def Creat_cs_entry(self, data, cs):
        '''
        cs = [[content_name, data, time, cost],...]
        cs_entry = [content_name, data, time, cost]
        data = {'type': 'data', 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0', 'content_data': '',
                'data_hop': 0, 'run_start_time': 0.0, 'path': ''}
        '''
        content_name = data['content_name']
        route_ID = data['route_ID']
        # content_data = data['content_data']
        # Record the time this entry was created
        # times = int(time.process_time()*1000 - data['run_start_time'])
        # cost = 0 # data['data_hop']

        cs_entry = [content_name, route_ID]  # , content_data, times, cost
        cs.append(cs_entry)
        # return cs_entry

        # Delete an entry from CS

    def Remove_cs_entry(self, cs, network_table):
        '''
        cs = [[content_name, data, time, cost],...]
        '''
        # self.cs = cs
        # cs.sort(key=lambda x:(x[-1]), reverse=False)

        # index = int(len(cs)/2)  # int(len(cs)/2)
        index = 0
        lens = []
        for i in range(len(cs)):
            if cs[i][1] > 11:
                continue
            lens.append(network_table[cs[i][1]])
        Min = min(lens[:])
        index = lens.index(Min)

        # Delete the most costly entry
        del cs[index]
        '''
        # 1  5  10  15  20  30  40  50
        if len(cs) != 0:
            temp = int(len(cs) * (update_cache / 100))
            for i in range(int((len(cs)-temp)/2), int((len(cs)+temp)/2)):
                index = i
                # Delete the most costly entry
                del cs[index]

        # 1  5  10  15  20  30  40  50
        if len(cs) != 0:
            temp = int(len(cs) * (update_cache / 100))
            for i in range(0, temp):
                index = i
                # Delete the most costly entry
                del cs[index]
        '''

        # Cache data

    def Cache_cs_data(self, cs, cache_size, data, network_table):
        '''
        cs = [[content_name, data, time, cost],...]
        data = {'type': 'data', 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0', 'content_data': '',
                'data_hop': 0, 'run_start_time': 0.0, 'path': ''}
        '''
        # self.cs = cs
        content_name = data['content_name']
        for cs_entry in cs:
            if content_name == cs_entry[0]:
                return
        # Check if CS is full
        if len(cs) > cache_size:
            # Remove the most costly entry
            self.Remove_cs_entry(cs, network_table)
        self.Creat_cs_entry(data, cs)
        # cs_entry =
        # cs.append(cs_entry)



    '''
    # Each router creates an independent cache space
    def Creat_cs(self, route_ID):

    # Get cs
    def Get_cs(self, route_ID):

    # Check if there is data matching the content name in cs
    def Search_cs_interest(self, cs, content_name):

    # Add an entry to CS
    def Creat_cs_entry(self, data, cs):


    # Delete an entry from CS
    def Remove_cs_entry(self, cs):

    # Cache data
    def Cache_cs_data(self, cs, cache_size, data):
    '''