from __future__ import print_function

from pit import PIT
from fib import FIB

class FORWARD():
    def __init__(self):
        self.forward = 0

    # Get data packet forwarding interface
    def Forward_data(self, pit, data):
        '''
        data = {'type': 'data', 'consumer_ID': 0, 'route_ID': 0, 'content_name': 'r0/0', 'content_data': '',
                'data_hop': 0, 'run_start_time': 0.0, 'path': ''}
        pit = {'content_name': [[inface, ...], [outface, ...]], ...}
        '''
        Infaces = []
        inface = data['route_ID']
        # Get the requested content name of the data packet
        content_name = data['content_name']
        # Get the pit_entry of this content_name
        Pit = PIT()
        pit_entry = pit[content_name]   # Pit.Get_pit_entry(content_name)
        for x in pit_entry[0]:
            if x != inface:
                Infaces.append(x)
        return Infaces

    # Get interest packet forwarding interface
    def Forward_interest(self, fib, network, route_ID, interest):


        Outfaces = []
        inface = interest['route_ID']
        '''
        for Outface in network['r'+str(route_ID)]:
            if Outface == inface:
                Outfaces.append(Outface)
        '''
        # Get the fibs record table of this router
        ################################################
        ''''''
        Fib = FIB()
        Outfaces = Fib.Search_fib_interest(fib, route_ID, network, interest)

        ################################################
        return Outfaces
