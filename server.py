import socket
import threading


class Server:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.clients = {}
        self.receive()

    def receive(self):
        while True:
            client, adress = self.socket.accept()
            print(f"Connected with {str(adress)}!")

            # if new client then ask for nickname
            client.send("NEWCLIENT".encode('utf-8'))
            nickName = client.recv(1024)
            self.clients[client] = nickName

            # Send notification to all connected clients
            self.broadcast(
                f"{nickName} connected to the server"
                .encode('utf-8'))
            client.send("Connected to the server".encode('utf-8'))

            # start thread
            thread = threading.Thread(target=self.handle(), args=(client,))
            thread.start()

    def broadcast(self, message):
        for client in self.clients.keys():
            client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except Exception as e:
                print(e)
                client.close()
                del self.clients[client]
                break


# define server ip and port
HOST = '127.0.0.1'
PORT = '9090'

server = Server()
