# -*- coding: UTF-8 -*-
# Author: Junbin Zhang
# E-mail: p78083025@ncku.edu.tw
# Update time: 2021.03.05

from __future__ import print_function

import time

from cs import CS
from pit import PIT
from fib import FIB
from forward import FORWARD

class DATA():
    def __init__(self):
        self.data = {}

    # Create a data packet
    def Create_data(self, route_ID, interest):
        '''
        interest = {'type': 'interest', 'interest_ID': 0, 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0',
                     'interest_hop': 0, 'life_hop': 5, 'run_start_time': 0.0, 'interest_start_time': 0.0, 'path': ''}
        data = {'type': 'data', 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0', 'content_data': '',
                'data_hop': 0, 'run_start_time': 0.0, 'path': ''}
        '''
        data = {'type': 'data', 'consumer_ID': 0, 'route_ID': 0, 'content_name': '', 'content_data': '',
                'data_hop': 0, 'run_start_time': 0, 'interest_start_time': 0, 'path': ''}
        #self.data = data
        data['type'] = 'data'
        data['consumer_ID'] = interest['consumer_ID']
        data['interest_ID'] = interest['interest_ID']
        data['route_ID'] = route_ID
        data['content_name'] = interest['content_name']
        content = interest['content_name'] + str(int(time.time()))
        data['content_data'] = content
        data['data_hop'] = 0
        data['run_start_time'] = interest['run_start_time']
        data['interest_start_time'] = interest['interest_start_time']
        data['path'] = 'p'
        return data

    # Pack the data packet to be sent and the output interface
    def Send_data(self, Infaces, route_ID, data):
        '''
        data = {'type': 'data', 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0', 'content_data': '',
                'data_hop': 0, 'run_start_time': 0.0, 'path': ''}
        Infaces = [Inface, ...]
        Datas = [[Inface, data], ...]
        '''
        Datas = []
        # Hop count plus 1
        data['data_hop'] += 1
        data['route_ID'] = route_ID
        # Record the transmission path
        data['path'] += str(route_ID)+'/'
        for i in range(len(Infaces)):
            Datas.append([Infaces[i], data])
        return Datas

    # data packet processing
    def On_data(self, sizes, route_ID, data, tables, result_save, threadLock, network_table):
        '''
        data = {'type': 'data', 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0', 'content_data': '',
                'data_hop': 0, 'run_start_time': 0.0, 'path': ''}
        sizes = [queue_size, cache_size, fib_size]
        tables = [self.network, self.ps, self.cs, self.pit, self.fib]
        '''
        Cs = CS()
        Pit = PIT()
        Fib = FIB()
        Forward = FORWARD()
        network, ps, cs, pit, fib = tables
        _, cache_size, fib_size = sizes
        consumer_ID = data['consumer_ID']
        #print(str(consumer_ID)+'-'+str(route_ID)+'= '+str(pit))
        # Check whether there is an entry matching the content name of the data packet in the pit
        PIT_search_ACK = Pit.Search_pit_data(pit, data)
        # data match in PIT
        if PIT_search_ACK:
            ############################################################

            Cs.Cache_cs_data(cs, cache_size, data, network_table)
            Fib.Update_fib_outface_data(fib, route_ID, fib_size, data)

            ############################################################
            if consumer_ID != route_ID:
                Infaces = Forward.Forward_data(pit, data)
                Pit.Remove_pit_entry(pit, data)
                Datas = self.Send_data(Infaces, route_ID, data)
                #print('data hit in PIT')
                return Datas
            else:
                #print('YES consumer')
                threadLock.acquire()
                result_save['response_time'] += time.process_time() - data['interest_start_time']
                threadLock.release()
                packet = []
                return packet
        # data miss in PIT
        else:
            ############################################################

            Cs.Cache_cs_data(cs, cache_size, data, network_table)
            Fib.Update_fib_outface_data(fib, route_ID, fib_size, data)

            ############################################################
            #print('data miss in PIT')
            packet = []
            return packet