import threading
import json
import socket
import queue
import time
from interests import INTEREST
from data import DATA
from ps import PS
from pit import PIT
from forward import FORWARD

def load_peremiters():
    with open('input2/peremiters.json', 'r') as file:
        data = file.read()
    parse = json.loads(data)
    return parse

def input_interests():
    with open('input2/interests.json', 'r') as file:
        data = file.read()
    parse = json.loads(data)
    return parse

class Server(threading.Thread):

    def __init__(self, serverID, sizes, producer_contents, run_start_time, network, HOST='127.0.0.1'):
        threading.Thread.__init__(self)
        self.HOST = HOST
        self.PORT_accept = 1000 + serverID
        self.PORT_interests = 2000 + serverID
        self.PORT_data = 3000 + serverID
        self.PORT_send = 4000 + serverID
        self.serverID = serverID
        self.network = network
        self.run_start_time = run_start_time
        self.sizes = sizes
        self.producer_contents = producer_contents

        #json data
        self.peremiters = load_peremiters()
        self.input_interests = input_interests()

        # interest and data queue
        self.interest_queue = queue.Queue(maxsize=self.sizes)
        self.data_queue = queue.Queue(maxsize=self.sizes)

        # parameters
        self.content_num = self.peremiters['content_num']
        self.frequency = self.peremiters['frequency']

        # interests from json
        self.interests = self.input_interests['r' + str(self.serverID)]

        # class objects
        self.interest = INTEREST()
        self.data = DATA()
        self.ps = PS()
        self.pit = PIT()
        self.forward = FORWARD()

        # create 
        self.ps.Create_ps(self.serverID, self.content_num, self.producer_contents)
        self.pit.Create_pit(self.serverID)

        # time
        self.start_time = time.time()
        self.end_time = time.time()
        self.flag = False
        self.run_time = self.peremiters['run_time']

    def run(self):
        accept = threading.Thread(target=self.accept) 
        interests = threading.Thread(target=self.interests_process)
        data = threading.Thread(target=self.data_process)
        accept.start()
        interests.start()
        data.start()
        self.start_network(self.run_start_time, self.frequency, self.content_num, self.serverID, self.interests)
        accept.join()
        interests.join()
        data.join()

    def start_network(self, run_start_time, frequency, content_num, route_num, interests):
        publish_count = 0
        while publish_count < content_num:
            packets = self.interest.Generate_interest(self.serverID, run_start_time, frequency, content_num, route_num, interests)
            for i in range(len(packets)):
                for j in range(len(self.network)):
                    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server.connect((self.HOST, 1000 + self.network[j]))
                    server.sendall(json.dumps(packets[i]).encode('utf-8'))
                    server.recv(1024)
                    server.close()
            if len(packets) != 0:
                self.pit.Create_pit_entry(packets[0])
                self.pit.Update_pit_outface(0, self.network, packets[0])
                publish_count += 1
            time.sleep(1)
            

    def accept(self):
        # monitor
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.HOST, self.PORT_accept))
        server.listen(11)
        recv_msg = 'recv'
        while True:
            time.sleep(1)
            conn, addr = server.accept()
            packet = conn.recv(1024)
            conn.sendall(recv_msg.encode())
            packet = json.loads(packet.decode('utf-8'))
            # determine the type of packet
            Type = packet['type']

            if Type == 'interest':
                if self.interest_queue.full():
                    self.interest.Drop_interest(self.serverID, packet)
                else:
                    self.interest_queue.put(packet)
            elif Type == 'data':
                if self.data_queue.full():
                    self.data.Drop_data(packet['route_ID'], packet)
                else:
                    self.data_queue.put(packet)


    def interests_process(self):
        # send interest 
        while True:
            if self.interest_queue.empty():
                continue
            else:
                packet = self.interest_queue.get()
                if self.interest.Time_out(packet):
                    self.interest.Drop_interest(self.serverID, packet)
                else:
                    data_packet = self.interest.On_interest(self.serverID, packet, self.ps.Get_ps())
                    # data_packet = modify interest packet or None
                    # if data_packet == None then 
                    if data_packet == None:
                        # determine if interest in pit
                        content_name = packet['content_name']
                        pit = self.pit.Get_pit()
                        if content_name in pit:
                            # if in, merge interest
                            self.pit.Merge_pit_entry(packet)
                        else:
                            # if not, forward interest
                            # forward the interest to neighbors
                            self.pit.Create_pit_entry(packet)
                            # packet_forward = [[where send, packet],...]
                            self.pit, packet_forward = self.interest.Send_interest(self.pit, self.network, self.serverID, packet)
                            for i in range(len(packet_forward)):
                                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                server.connect((self.HOST, 1000 + packet_forward[i][0]))
                                server.sendall(json.dumps(packet_forward[i][1]).encode('utf-8'))
                                server.recv(1024)
                                server.close()
                            # add outfaces to pit entry
                            self.pit.Update_pit_outface(0, self.network, packet)

                    # if data_packet != None
                    else:
                        # send the data packet
                        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server.connect((self.HOST, 1000 + data_packet[0]))
                        server.sendall(json.dumps(data_packet[1]).encode('utf-8'))
                        server.recv(1024)
                        server.close()
                        

    def data_process(self):
        # send data
        while True:
            if self.data_queue.empty():
                continue
            else:
                packet = self.data_queue.get()
                # determine if data in pit
                content_name = packet['content_name']
                pit = self.pit.Get_pit()
                if self.data.On_data(0, self.serverID, packet, pit):
                    # return True if need forward
                    infaces = pit[content_name][0]
                    packet_forward = self.data.Send_data(infaces, self.serverID, packet)
                    for i in range(len(packet_forward)):
                        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server.connect((self.HOST, 1000 + packet_forward[i][0]))
                        server.sendall(json.dumps(packet_forward[i][1]).encode('utf-8'))
                        server.recv(1024)
                        server.close()
                    self.pit.Remove_pit_entry(pit, packet)
                else:
                    # return False if not need forward
                    self.pit.Remove_pit_entry(pit, packet)