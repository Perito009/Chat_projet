class ChatRoom:
    def __init__(self, name):
        self.name = name
        self.clients = {}

    def add_client(self, client, nickname):
        self.clients[client] = nickname
        self.broadcast(f"{nickname} a rejoint le salon {self.name}!")

    def remove_client(self, client):
        nickname = self.clients.pop(client, None)
        if nickname:
            self.broadcast(f"{nickname} a quitté le salon {self.name}.")

    def broadcast(self, message, sender=None):
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(client)
