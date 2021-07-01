from network import NETWORK
import json
import queue
def load_network():
    with open('./Input/network.json', 'r', encoding='utf8') as fp:
        network = json.load(fp)
    return network

Net = NETWORK()
network = load_network()


table, path = Net.Bulid_network_graph(11, network)


q = queue.Queue()

q.put(1)
q.put(2)
q.put(3)

a = q.queue[1]

q.queue.remove(a)

print(q.queue)
