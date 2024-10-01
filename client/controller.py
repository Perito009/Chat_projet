from .view import ChatGUI
from .model import ClientNetwork

class ChatController:
    def __init__(self):
        self.nickname = None
        self.network = None
        self.view = None

    def start(self):
        self.view = ChatGUI(self)
        self.view.get_nickname(self.set_nickname)

    def set_nickname(self, nickname):
        self.nickname = nickname
        self.network = ClientNetwork(self.nickname)
        self.network.start_receiving(self.update_chat)
        self.view.setup_main_window()

    def send_message(self, message):
        if message:
            self.network.send_message(message)

    def join_room(self, room):
        if room:
            self.network.join_room(room)

    def update_chat(self, message):
        # Déterminez si le message vient de l'utilisateur ou d'un autre
        is_own_message = message.startswith(f"{self.nickname}:")
        self.view.update_chat(message, is_own_message)

    def disconnect(self):
        if self.network:
            self.network.disconnect()

    def run(self):
        self.start()
        self.view.run()
