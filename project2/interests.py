import csv
import time
from pit import PIT


class INTEREST():
    # database of interest
    def __init__(self):
        self.publish_count = 0

    def Generate_interest(self, route_ID, run_start_time, frequency, content_num, route_num, interest):
        # generate frequency/sec interest packet part
        # and return to server
        packets = []
        if self.publish_count >= content_num:
            return packets

        # data from interset json
        interest_ID = interest[self.publish_count]['interest_ID']
        consumer_ID = route_ID
        content_name = interest[self.publish_count]['content_name']

        for i in range(frequency):
            # pack the packet
            packet = {}
            packet['type'] = 'interest'
            packet['interest_ID'] = interest_ID
            packet['consumer_ID'] = consumer_ID
            packet['route_ID'] = route_ID
            packet['content_name'] = content_name
            packet['interest_hop'] = 0
            packet['run_start_time'] = run_start_time
            packet['path'] = 'p' + str(route_ID)
            packets.append(packet)
            self.publish_count += 1

        # return a list contain 'frequency' packets to server
        return packets

    def Time_out(self, interest):
        # argument interest is a interset packet
        if interest['interest_hop'] >= 5:
            return True
        else:
            return False

    def Send_interest(self, pit, Outfaces, route_ID, interest):
        # forward interset packet
        # argument interest is interest packet
        interest['route_ID'] = route_ID
        interest['path'] += '/' + str(route_ID)
        interest['interest_hop'] += 1

        # add this interest to PIT
        # argument pit set to 0
        pit.Update_pit_outface(0, Outfaces, interest)

        interests = []
        for i in Outfaces:
            interests.append([i, interest])

        return pit, interests

    def On_interest(self, route_ID, interest, tables):
        # determine whether the content name in PS
        content_name = interest['content_name']
        packet = {}
        if content_name in tables:
            current_time = 0
            packet['type'] = 'data'
            packet['consumer_ID'] = interest['consumer_ID']
            packet['route_ID'] = route_ID
            packet['content_name'] = interest['content_name']
            packet['content_data'] = interest['content_name'] + str(current_time)
            packet['data_hop'] = 1
            packet['run_start_time'] = interest['run_start_time']
            packet['path'] = 'p' + str(route_ID)
            # if hit return a data packet to server and output hit to output.csv
            result = 'interest hits in ps'
            self.Output_interest_txt(interest, 0, result, 1, 0)
            # return [where send, data packet]
            return [interest['route_ID'], packet]
        # if miss output miss to output.csv
        else:
            result = 'interest miss in ps'
            self.Output_interest_txt(interest, 0, result, 0, 1)

            return None

    def Output_interest_txt(self, interest, times, result, hit, miss):
        table = ['Time', 'Type', 'Interest_ID', 'Consumer_ID', 'Route_ID',
                 'Content_name', 'Interest_hop', 'Path', 'Result', 'Hit', 'Miss']
        interests_csv = {
            'Time': str(int(time.time() - interest['run_start_time'])),
            'Type': interest['type'],
            'Interest_ID': 'I' + str(interest['interest_ID']),
            'Consumer_ID': 'C' + str(interest['consumer_ID']),
            'Route_ID': 'R' + str(interest['route_ID']),
            'Content_name': interest['content_name'],
            'Interest_hop': interest['interest_hop'],
            'Path': interest['path'],
            'Result': result,
            'Hit': hit,
            'Miss': miss,
        }
        file = open('Output_interest.csv', 'a', newline='')
        writer = csv.DictWriter(file, fieldnames=table)
        writer.writerow(interests_csv)
        file.close()

    def Drop_interest(self, route_ID, interest):
        # output packet information and write drop message to csv
        result = 'drop interest'
        self.Output_interest_txt(interest, 0, result, 0, 1)
