import socket
import threading
from shared.constants import HOST, PORT


class ClientNetwork:
    def __init__(self, nickname):
        self.nickname = nickname
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.client.send(nickname.encode('utf-8'))

    def send_message(self, message):
        self.client.send(f"{self.nickname}: {message}".encode('utf-8'))

    def join_room(self, room):
        self.client.send(f"JOIN:{room}".encode('utf-8'))

    def receive_messages(self, callback):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                callback(message)
            except:
                print("Une erreur est survenue!")
                self.client.close()
                break

    def start_receiving(self, callback):
        thread = threading.Thread(target=self.receive_messages, args=(callback,))
        thread.daemon = True
        thread.start()

    def disconnect(self):
        self.client.close()
