import json
import socket
import sys
import threading
import time


def client(server_num, message):
    HOST = '127.0.0.1'
    PORT = 7000 + server_num

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    outdata = message
    print('send: ' + outdata + ' to ' + str(server_num))
    s.send(outdata.encode())
    indata = s.recv(1024)
    print(indata.decode())
    s.close()
    return


def server(server_num, stop_event):

    HOST = '127.0.0.1'
    PORT = 7000 + server_num

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    print('server start at: %s:%s' % (HOST, PORT))
    print('wait for connection...')

    while not stop_event.is_set():
        conn, addr = s.accept()
        # print('connected by ' + str(addr))

        while not stop_event.is_set():
            indata = conn.recv(1024)
            conn.send("receive success".encode())

            if(indata.decode() == 'Start'):
                tthreads = []
                print('I am number:'+str(server_num)+' start to pass')

                for i in range(len(data["input"])):
                    for j in range(len(data["input"][i])):
                        if(data["input"][i][j][0] == server_num):
                            if data["input"][i][j][1] in data["network"][server_num][1]:
                                tt = threading.Thread(target=client, args=(
                                    data["input"][i][j][1], data["input"][i][j][2]))
                                tt.start()
                                time.sleep(1)
                                tt.join()
                            else:
                                print("server_num"+str(server_num) + " " +
                                      str(data["input"][i][j])+" Unreachable")
                                ff = open('output.txt', 'a')
                                ff.write('r' + str(server_num) +
                                         ' : ' + str(data["input"][i][j])+"Unreachable\n")
                                ff.close()

            if len(indata) == 0:  # connection closed
                conn.close()
                print('client closed connection.')
                break
            print('server_num ' + str(server_num) +
                  ' : recv: ' + indata.decode())
            if(indata.decode() != 'Start'):
                ff = open('output.txt', 'a')
                ff.write('r' + str(server_num) +
                         ' : ' + indata.decode()+"\n")
                ff.close()

    conn.send("client end".encode())
    print("server end")


if __name__ == "__main__":
    input = 'input.json'
    barrier = threading.Barrier(5)
    finish = threading.Event()
    with open(input) as f:
        data = json.load(f)
    t_list = []

    ff = open('output.txt', 'w')
    ff.write("")
    ff.close()

    for i in range(len(data["network"])):
        t = threading.Thread(target=server, args=(i, finish))
        t_list.append(t)
        t_list[i].start()
    print(threading.active_count())

    time.sleep(2)

    threads = []
    for i in range(len(data["network"])):
        threads.append(threading.Thread(
            target=client, args=(i, 'Start')))
        threads[i].start()
        time.sleep(5)

    for t in threads:
        t.join()

    print(threading.active_count())
    finish.set()

    threads = []
    for i in range(len(data["network"])):
        threads.append(threading.Thread(
            target=client, args=(i, 'End')))
        threads[i].start()

    for t in threads:
        t.join()
        time.sleep(1)

    print(finish.is_set())
    for t in t_list:
        t.join()
        time.sleep(1)

    print(threading.active_count())

    print('finish')
