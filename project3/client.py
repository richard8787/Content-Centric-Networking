import socket

class Client:

    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 8001

    def start_client(self):
        clientMessage = 'Hello!'
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client.connect((self.HOST, self.PORT))
        
        client.sendall(clientMessage.encode())

        serverMessage = str(client.recv(1024), encoding='utf-8')
        print('Server:', serverMessage)

        client.close()

if __name__ == '__main__':
    client = Client()
    client.start_client()