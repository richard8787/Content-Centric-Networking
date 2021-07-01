from __future__ import print_function

import time

from network import NETWORK

'''
def Creat_FIB(self, route_ID):

def Get_fib(self, route_ID):

def Get_fib_entry(self, fib, content_name):

def Add_fib_outface(self, data, route_ID, fib_entry):

# Remove the content name with the most cost
def Remove_fib_entry(self,fib):

def Add_fib_entry(self, fib, data, route_ID):

# The outface is updated to fib
def Update_fib_outface_data(self, fib, route_ID, fib_size, data):

# Forward interest packets to all neighbors
def Broadcast(self, route_ID, inface):

# Choose the outface with the min cost to forward the interest packet
def Best_route(self, route_ID, inface, fib_entry):

# Find in FIB whether there is a matching interest packet entry
def Search_fib_interest(self, fib, route_ID, interest):
'''

class FIB():
    def __init__(self):
        self.fib = {}
        self.fib_entry = []

    def Creat_FIB(self, route_ID):
        '''
        fib = {'content_name': [[outface, cost, time], ...],
               ...
               }
        '''
        return self.fib


    def Get_fib(self, route_ID):
        '''
        fib = {'content_name': [[outface, cost, time], ...],
               ...
               }
        '''
        return self.fib


    def Get_fib_entry(self, fib, content_name):
        '''
        fib = {'content_name': [[outface, cost, time], ...], ... }
        fib_entry = [[oufibtface, cost, time], ...]
        '''
        # self.fib_entry = self.fib.get(key=content_name, default=None)
        # self.fib = fib
        if content_name in fib:
            fib_entry = fib[content_name]
            return fib_entry
        else:
            return []


    def Add_fib_outface(self, data, route_ID, fib_entry):
        '''
        data = {'type': 'data', 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0', 'content_data': '',
                'data_hop': 0, 'run_start_time': 0.0, 'path': ''}
        fib = {'content_name': [[outface, cost, time], ...], ... }
        fib_entry = [[outface, cost, time], ...]
        '''
        outface = data['route_ID']
        # cost = abs(entry[1] - i)    # data['data_hop']
        # Record the time when the outface was added
        times = int(time.process_time())  # time.clock()
        cost = data['data_hop']
        for entry in fib_entry:
            if entry[0] == outface:
                if cost < entry[1]:
                    entry[1] = cost
                    entry[2] = times
                    # Sort by cost from smallest to largest
                    fib_entry.sort(key=lambda x: (x[1]), reverse=False)
                return
        if len(fib_entry) < 1000:
            fib_entry.append([outface, cost, times])
        else:
            # Delete the most costly outface
            x = fib_entry.pop(-1)
            fib_entry.append([outface, cost, times])
        # Sort by cost from smallest to largest
        fib_entry.sort(key=lambda x: (x[1]), reverse=False)

        # Remove the content name with the most cost


    def Remove_fib_entry(self, fib):
        '''
        fib = {'content_name': [[outface, cost, time], ...], ... }
        '''
        # max = 0
        # content_name = ''
        # self.fib = fib
        # Find the content name with the most cost
        for key, value in fib.items():
            # if len(value) > 0:
            #     cost = value[0][1]
            # time = value[0][2]
            #     if cost > max:
            #         max = cost
            #         content_name =
            # if max != 0:content_name
            del fib[key]
            break


    def Add_fib_entry(self, fib, data, route_ID):
        '''
        data = {'type': 'data', 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0', 'content_data': '',
                'data_hop': 0, 'run_start_time': 0.0, 'path': ''}
        fib = {'content_name': [[outface, cost, time], ...], ... }
        fib_entry = [[outface, cost, time], ...]
        '''
        # self.fib = fib
        content_name = data['content_name']
        outface = data['route_ID']
        times = int(time.process_time())  # time.clock()
        cost = data['data_hop']
        temp = {content_name: [[outface, cost, times]]}
        fib.update(temp)

        # The outface is updated to fib


    def Update_fib_outface_data(self, fib, route_ID, fib_size, data):
        '''
        fib = {'content_name': [[outface, cost, time], ...], ... }
        fib_entry = [[outface, cost, time], ...]
        '''
        # self.fib = fib
        content_name = data['content_name']
        fib_entry = self.Get_fib_entry(fib, content_name)
        if len(fib_entry) == 0:
            if len(fib) > fib_size:
                self.Remove_fib_entry(fib)
            self.Add_fib_entry(fib, data, route_ID)
        else:
            self.Add_fib_outface(data, route_ID, fib_entry)

        # Forward interest packets to all neighbors


    def Broadcast(self, route_ID, network, inface):
        Outfaces = []
        Network = NETWORK()
        network = Network.Get_network(network)
        entry = network['r' + str(route_ID)]
        for outface in entry:
            '''
            if route_ID == 7:
                Outfaces.append([outface,1])      # outfaces=[[outface,cost],...]
            el
            '''
            if outface != inface and outface != route_ID:  #
                Outfaces.append([outface, 1])  # outfaces=[[outface,cost],...]
        return Outfaces

        # Choose the outface with the min cost to forward the interest packet


    def Best_route(self, route_ID, network, inface, fib_entry):
        Outface = []

        for entry in fib_entry:
            outface = entry[0]
            if outface != inface and outface != route_ID:  #
                cost = entry[1]
                Outface.append([outface, cost])  # outfaces=[[outface,cost],...]
                return Outface
        if len(Outface) == 0:
            Outface = self.Broadcast(route_ID, network, inface)
        return Outface

        # Find in FIB whether there is a matching interest packet entry


    def Search_fib_interest(self, fib, route_ID, network, interest):
        '''
        interest = {'type': 'interest', 'interest_ID': 0, 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0',
                    'interest_hop': 0, 'life_hop': 5, 'run_start_time': 0.0, 'path': ''}
        fib = {'content_name': [[outface, cost, time], ...], ... }
        '''
        content_name = interest['content_name']
        inface = interest['route_ID']
        fib_entry = self.Get_fib_entry(fib, content_name)

        if len(fib_entry) == 0:
            Outfaces = self.Broadcast(route_ID, network, inface)
        else:
            # print(str(fib_entry) + ' ')
            Outfaces = self.Best_route(route_ID, network, inface, fib_entry)
        # print(str(inface) + '-' + str(route_ID) + '= ' + str(Outfaces))
        # print(str(Outfaces) + '-' + str(Outfaces_temp)+' ')
        # print(str(Outfaces_temp) + ' ')
        return Outfaces
