from server import TServer
import time
import threading
import queue
import socket

#平行接收
class Server_accept(threading.Thread):
  def __init__(self, conn, addr, serverID):
    threading.Thread.__init__(self)
    self.socket = conn
    self.address = addr
    self.serverID = serverID

  def run(self):
    while True:
      try:
        clientMessage = str(self.socket.recv(1024), encoding='utf-8')
        if not clientMessage:
          break
        print('Client message is:', clientMessage)
        serverMessage = 'I\'m here! ' + str(self.serverID)
        self.socket.sendall(serverMessage.encode())
      except self.socket.timeout:
        break
    self.socket.close()

class TBind(threading.Thread):
  def __init__(self, socket, address):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    self.socket = socket
    self.address = address

  def run(self):
    #Each port will create a connection until the data passing complete
    self.server.bind((self.socket, self.address))
    self.server.listen(10)
    while True:
      conn, addr = self.server.accept()
      Server_accept(conn, addr, self.serverID).start()

class TServer(threading.Thread):
  def __init__(self, serverID, lock):
      threading.Thread.__init__(self)
      self.socket = '127.0.0.1'
      self.address= 8000 + serverID
      self.serverID = 'r' + str(serverID)
      self.lock = lock
      
      #FIB
      self.network = [['r0', ['r1', 'r3']], ['r1', ['r0', 'r2', 'r3']], ['r2', ['r1', 'r5']], ['r3', ['r0', 'r1', 'r4']],
       ['r4', ['r3', 'r5', 'r6']], ['r5', ['r2', 'r4', 'r7']], ['r6', ['r4', 'r7', 'r11']], ['r7', ['r5','r6','r8','r9']],
       ['r8', ['r7']], ['r9', ['r7', 'r11']], ['r10', ['r6', 'r11']], ['r11', ['r9', 'r10']]]

  def run(self):   
    #use thread to create multiple port with listen
    list = self.network[self.serverID][1][:]
    end_list = []

    for next in len(list):
      thread_bind = TBind(self.socket, next)
      thread_bind.start()
      end_list.append(thread_bind)
      

if __name__ == "__main__":
  server_num = 3    #node num
  threads = []
  q = queue.Queue()
  lock = threading.Lock()

  for i in range(server_num):
    thread = TServer(i,lock)    #create node with thread
    thread.start()
    threads.append(thread)
  
  # for thread in threads:
  #   thread.join()