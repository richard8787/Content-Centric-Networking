
import time
import json

from server import Server, result_save

# Read network
def load_network():
    with open('./Input/network.json', 'r', encoding='utf8') as fp:
        network = json.load(fp)
    return network

# Read parameters
def load_peremiters():
    with open('./Input/peremiters.json', 'r', encoding='utf8') as fp:
        peremiters = json.load(fp)
    return peremiters

# Read the contents produced by each producer
def input_producer_contents():
    with open('./Input/producer_contents.json', 'r', encoding='utf8') as fp:
        producer_contents = json.load(fp)
    return producer_contents

# Read the interest packets to be sent by each router
def input_interests():
    with open('./Input/interests.json', 'r', encoding='utf8') as fp:
        interests = json.load(fp)
    return interests

def main(producer_contents,interests, peremiters, network):
    '''
    peremiters = {"route_num": ,      # Number of routers
                  "frequency": ,       # How many interest packets sent by each router to the network per second
                  "content_num": ,   # The amount of content produced by each producer
                  "run_time": ,       # Simulator running time
                  "queue_size": ,     # The storage space size of the queue
                  "cache_size": ,     # CS storage space size
                  "FIB_size": }       # FIB storage space size
    '''
    server_num = peremiters['route_num']
    frequency = peremiters['frequency']
    route_num = peremiters['route_num']
    content_num = peremiters['content_num']
    run_time = peremiters['run_time']
    queue_size = peremiters['queue_size']
    cache_size = peremiters['cache_size']
    fib_size = peremiters['fib_size']

    sizes = [queue_size, cache_size, fib_size]
    # Get the start time of the simulator
    run_start_time = time.process_time()
    server_list = []
    for i in range(server_num):
        server = Server(i, sizes, producer_contents, run_start_time, network)
        server.start()
        server_list.append(server)
    while True:
        # The router sends new interest packets to the network
        for i in server_list:
            i.start_network(run_start_time, frequency, content_num, route_num, interests)
        # Is the simulator running time up
        if time.process_time() - run_start_time > run_time:
            # Output simulator running time
            print('cache_hit_rate = ' + str(float(result_save["cache_hit_cs"] / ( result_save["cache_hit_cs"] + result_save["cache_miss_cs"]))))
            print('average_response_time = ' + str(float(result_save["response_time"] / result_save["send_interest"])))
            print(' ')
            print('end')
            for i in server_list:
                i.join()
            break

if __name__ == '__main__':
    paramiters = load_peremiters()
    producer_contents = input_producer_contents()
    interests = input_interests()
    network = load_network()
    main(producer_contents,interests, paramiters, network)

