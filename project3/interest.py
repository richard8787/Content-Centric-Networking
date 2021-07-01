# -*- coding: UTF-8 -*-
# Author: Junbin Zhang
# E-mail: p78083025@ncku.edu.tw
# Update time: 2021.03.05

from __future__ import print_function

import time

from pit import PIT
from ps import PS
from cs import CS
from fib import FIB
from data import DATA
from forward import FORWARD

class INTEREST():
    def __init__(self):
        self.interest = {}
        self.interest_table = []

        # Consumer generated interest packet
    def Generate_interest(self, route_ID, run_start_time, interest, result_save,threadLock):
        #interest = {'interest_ID': 00000,'content_name':'r1/3'}
        #interest_temp = {'type': 'interest', 'interest_ID': 0, 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0',
                     #'interest_hop': 0, 'life_hop': 5, 'run_start_time': 0.0, 'path': ''}
        Interests = []
        for i in range(0, len(interest)):

            interest_temp = {'type': "interest", 'interest_ID': '', 'consumer_ID': 0, 'route_ID': 0, 'content_name': '',
                             'interest_hop': 0, 'life_hop': 0, 'run_start_time': 0.0, 'interest_start_time': 0.0,
                             'path': ''}
            interest_temp['type'] = 'interest'
            interest_temp['interest_ID'] = interest[i]['interest_ID']
            interest_temp['consumer_ID'] = route_ID
            interest_temp['route_ID'] = route_ID
            interest_temp['content_name'] = interest[i]['content_name']
            interest_temp['interest_hop'] = 0
            interest_temp['life_hop'] = 12
            interest_temp['run_start_time'] = run_start_time
            interest_temp['interest_start_time'] = time.process_time()
            interest_temp['path'] = 'p'+str(route_ID)+'/'
            Interests.append(interest_temp)
            threadLock.acquire()
            result_save["send_interest"] += 1
            threadLock.release()
        return Interests

    # Check whether the interest packet has timed out
    def Time_out(self, interest,provider_save,threadLock):
        '''
        '''
        interest_hop = interest['interest_hop']
        life_hop = interest['life_hop']
        if interest_hop < life_hop:
            return True
        else:
            # Drop interest
            return False

    # Pack the interest packet to be sent and the output interface
    def Send_interest(self, pit, fib, Outfaces, route_ID, interest):
        '''
        Outfaces = [outface, ...]
        '''
        # Send interest
        Interests = []
        interest['route_ID'] = route_ID
        # Hop count plus 1
        interest['interest_hop'] += 1
        # Record the transmission path
        interest['path'] += str(route_ID)+'/'
        #print('Outfaces = '+str(Outfaces))
        #if len(Outfaces_temp) > 0:
        #    print('Outfaces_temp = ' + str(Outfaces_temp))
        for i in range(len(Outfaces)): # Outfaces=[[Outface,cost],...]
            Outface=Outfaces[i][0]
            Interests.append([Outface, interest])
        # The outface is updated to pit
        Pit = PIT()
        Pit.Update_pit_outface(pit, Outfaces, interest)
        #print(str(len(interest_table))+' ')
        return Interests

    # Interest packet processing
    def On_interest(self, route_ID, interest, tables,sizes,result_save,threadLock):
        '''
        interest =
        data =
        '''
        Ps = PS()
        Cs = CS()
        Pit = PIT()
        Fib = FIB()
        Data = DATA()
        Forward = FORWARD()
        Interest = INTEREST()
        network, ps, cs, pit, fib = tables
        _, cache_size, fib_size = sizes
        #self.interest_table=interest_table
        content_name = interest['content_name']
        #print(str(interest['consumer_ID'])+'-'+str(route_ID)+'= '+str(cs))
        # Find the data of the content name in ps
        Search_ps_ACK = Ps.Search_ps_interest(ps, content_name)
        # interest hit in ps
        if Search_ps_ACK == True:
            # Return data packet
            data = Data.Create_data(route_ID, interest)
            inface = [interest['route_ID']]
            Datas = Data.Send_data(inface, route_ID, data)
            # print('interest hit in PS')
            return Datas
        # interest miss in ps
        else:
            #print('interest miss in PS')
            ########################################################

            # If the data required for the interest packet is not found in the PS, go to the CS to find it.
            Search_cs_ACK = Cs.Search_cs_interest(cs, content_name)
            # interest hit in CS
            if Search_cs_ACK == True:
                consumer_ID = interest['consumer_ID']
                threadLock.acquire()
                result_save['cache_hit_cs'] += 1
                threadLock.release()
                if consumer_ID == route_ID:
                    # print(str(route_ID)+'YES consumer'+' ')
                    threadLock.acquire()
                    result_save['response_time'] += time.process_time() - interest['interest_start_time']
                    threadLock.release()
                    packet = []
                    return packet
                # Return data packet
                data = Data.Create_data(route_ID, interest)
                inface = [interest['route_ID']]
                Datas = Data.Send_data(inface, route_ID, data)
                #print('interest hit in CS')
                return Datas
            else:
                # print('interest miss in CS')
                threadLock.acquire()
                result_save['cache_miss_cs'] += 1
                threadLock.release()

            ########################################################

        # Check whether there is an entry matching the content name of the interest packet in the pit
        Search_pit_ACK = Pit.Search_pit_interest(pit, interest, route_ID)
        # interest miss in PIT
        if Search_pit_ACK == True:
            # Forward the interest packet to the next router
            Outfaces = Forward.Forward_interest(fib, network, route_ID, interest)
            if len(Outfaces)>0:
                Interests = self.Send_interest(pit, fib, Outfaces, route_ID, interest)
                #print('interest miss in PIT')
                return Interests
        packet = []
        return packet
        # interest match in PIT
        #else:
