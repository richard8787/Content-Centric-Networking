import csv
import time


class DATA():
    def __init__(self):
        self.data_package = {}

    def Create_data(self, route_ID, interest):
        times = 0
        self.data_package['type'] = 'data'
        self.data_package['consumer_ID'] = interest['consumer_ID']
        self.data_package['route_ID'] = route_ID
        self.data_package['content_name'] = interest['content_name']
        # content data = random number
        self.data_package['content_data'] = ''
        self.data_package['data_hop'] = 0
        self.data_package['start_time'] = times
        self.data_package['path'] = 'p' + str(route_ID)

        return self.data_package

    def Send_data(self, Infaces, route_ID, data):
        packets = []
        for i in range(len(Infaces)):
            data['data_hop'] += 1
            data['path'] += '/' + str(route_ID)
            data['route_ID'] = route_ID
            packets.append([Infaces[i], data])
        return packets

    def On_data(self, sizes, route_ID, data, tables):
        # tables is PIT
        # check if data in PIT
        content_name = data['content_name']
        if content_name in tables:
            consumer_ID = data['consumer_ID']
            # check if route ID is the same as consumer ID
            # if yes
            if consumer_ID == route_ID:
                # output data hit in consumer to csv
                result = 'data hit in consumer'
                self.Output_data_txt(data, 0, result, 1, 1, 0)
            # if not
            else:
                # output date hit in PIT to csv
                result = 'data hit in pit'
                self.Output_data_txt(data, 0, result, 0, 1, 0)
                # and forward data packet
                # return True when forward
                return True
        # if data not in PIT
        else:
            # output data miss to csv
            result = 'data miss in pit'
            self.Output_data_txt(data, 0, result, 0, 0, 1)
            self.Drop_data(0, data)
        # return False when it is unnecessary to forward
        return False

    def Drop_data(self, inface, data):
        # output drop information to csv
        result = 'drop data'
        self.Output_data_txt(data, 0, result, 0, 0, 1)

    def Output_data_txt(self, data, times, result, hit_consumer, hit_PIT, miss_PIT):
        # output hit or miss in PIT or consumer
        # TODO
        table = ['Time', 'Type', 'Consumer_ID', 'Route_ID', 'Content_name',
                 'Data_hop', 'Path', 'Result', 'Hit_consumer', 'Hit_PIT', 'Hit_Miss']
        data_csv = {
            'Time': str(int(time.time() - data['run_start_time'])),
            'Type': data['type'],
            'Consumer_ID': 'C' + str(data['consumer_ID']),
            'Route_ID': 'R' + str(data['route_ID']),
            'Content_name': data['content_name'],
            'Data_hop': data['data_hop'],
            'Path': data['path'],
            'Result': result,
            'Hit_consumer': hit_consumer,
            'Hit_PIT': hit_PIT,
            'Hit_Miss': miss_PIT,
        }
        file = open('Output_data.csv', 'a', newline='')
        writer = csv.DictWriter(file, fieldnames=table)
        writer.writerow(data_csv)
        file.close()
