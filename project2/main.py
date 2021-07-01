from server import Server
import json
import threading
import time
import csv


def load_network():
    with open('input2/network.json', 'r') as file:
        data = file.read()
    parse = json.loads(data)
    return parse


def load_peremiters():
    with open('input2/peremiters.json', 'r') as file:
        data = file.read()
    parse = json.loads(data)
    return parse


def input_producer_contents():
    with open('input2/producer_contents.json', 'r') as file:
        data = file.read()
    parse = json.loads(data)
    return parse


def input_interests():
    with open('input2/interests.json', 'r') as file:
        data = file.read()
    parse = json.loads(data)
    return parse


def main():
    ff = open('Output_data.csv', 'w')
    ff.truncate()
    ff.close()
    ff = open('Output_interest.csv', 'w')
    ff.truncate()
    ff.close()

    table = ['Time', 'Type', 'Consumer_ID', 'Route_ID', 'Content_name',
             'Data_hop', 'Path', 'Result', 'Hit_consumer', 'Hit_PIT', 'Hit_Miss']
    file = open('Output_data.csv', 'a', newline='')
    writer = csv.DictWriter(file, fieldnames=table)
    writer.writeheader()
    file.close()

    table = ['Time', 'Type', 'Interest_ID', 'Consumer_ID', 'Route_ID',
             'Content_name', 'Interest_hop', 'Path', 'Result', 'Hit', 'Miss']
    file = open('Output_interest.csv', 'a', newline='')
    writer = csv.DictWriter(file, fieldnames=table)
    writer.writeheader()
    file.close()

    network = load_network()
    peremiters = load_peremiters()
    producer_contents = input_producer_contents()
    intersets = input_interests()

    sizes = peremiters['queue_size']
    # run server
    servers = []
    for i in range(len(network)):
        server_name = "r"+str(i)
        server = Server(
            i, sizes, producer_contents[server_name], time.time(), network[server_name])
        server.start()
        servers.append(server)
    for i in range(len(servers)):
        servers[i].join()


if __name__ == '__main__':
    main()
