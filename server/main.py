import socket
import threading
from server.room import ChatRoom
from shared.constants import HOST, PORT


class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.rooms = {'general': ChatRoom('general')}

    def handle_client(self, client):
        nickname = client.recv(1024).decode('utf-8')
        current_room = self.rooms['general']
        current_room.add_client(client, nickname)
        
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if message.startswith('JOIN:'):
                    room_name = message.split(':')[1]
                    if room_name not in self.rooms:
                        self.rooms[room_name] = ChatRoom(room_name)
                    current_room.remove_client(client)
                    current_room = self.rooms[room_name]
                    current_room.add_client(client, nickname)
                else:
                    current_room.broadcast(message, client)
            except:
                current_room.remove_client(client)
                client.close()
                break

    def run(self):
        self.server.listen()
        print(f"Serveur en écoute sur {HOST}:{PORT}")
        while True:
            client, address = self.server.accept()
            print(f"Nouvelle connexion de {address}")
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.run()
