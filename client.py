import socket
import threading
import sys


class Client:
    def __init__(self, HOST, PORT, nickName, password):
        self.HOST = HOST
        self.PORT = PORT
        self.nickName = nickName
        self.password = password
        self.alive = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.start_threads()

    def receive(self):
        while self.alive:
            try:
                message = self.socket.recv(1024).decode("utf-8")
                if message == "NEWCLIENT":
                    self.socket.send(self.nickName.encode("utf-8"))
                    self.socket.send(self.password.encode("utf-8"))
                elif message != "":
                    print(message)
                else:
                    self.socket.close()

            except:
                print("an error occured")
                self.socket.close()
                self.alive = False
                sys.exit()

    def sendMsg(self):
        while self.alive:
            message = input()
            self.socket.send(message.encode("utf-8"))

    def start_threads(self):
        # start receive thread
        self.receiveThread = threading.Thread(target=self.receive)
        self.receiveThread.start()

        # start send thread
        self.sendThread = threading.Thread(target=self.sendMsg)
        self.sendThread.start()


HOST = '127.0.0.1'
PORT = 9090
nickName = input("Insert your nickname: ")
password = input("Insert your password: ")
client = Client(HOST, PORT, nickName, password)
