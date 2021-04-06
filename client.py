import socket
import threading


class Client:
    def __init__(self, HOST, PORT, nickName):
        self.HOST = HOST
        self.PORT = PORT
        self.nickName = nickName
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.start_threads()

    def receive(self):
        while True:
            try:
                message = self.socket.recv(1024).decode("utf-8")
                if message == "NEWCLIENT":
                    self.socket.send(self.nickName.encode("utf-8"))
                else:
                    print(message)
            except Exception as e:
                print(e)
                self.socket.close()
                break

    def sendMsg(self):
        while True:
            message = input()
            self.socket.send(message.encode("utf-8"))

    def start_threads(self):
        # start receive thread
        receiveThread = threading.Thread(target=self.receive)
        receiveThread.start()

        # start send thread
        sendThread = threading.Thread(target=self.sendMsg)
        sendThread.start()


HOST = '127.0.0.1'
PORT = 9090
nickName = input("Insert your nickname: ")
client = Client(HOST, PORT, nickName)
