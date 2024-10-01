import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatGUI:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()

        # Configuration de la zone de texte
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=20)
        self.chat_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.chat_area.config(state='disabled')

        # Configuration du champ d'entrée pour les messages
        self.msg_entry = tk.Entry(self.root, width=30)
        self.msg_entry.pack(padx=10, pady=5, side=tk.LEFT, expand=True, fill=tk.X)

        # Configuration du bouton d'envoi
        self.send_button = tk.Button(self.root, text="Envoyer", command=self.send_message)
        self.send_button.pack(padx=10, pady=5, side=tk.RIGHT)

        # Configuration du champ d'entrée pour les salons
        self.room_entry = tk.Entry(self.root, width=20)
        self.room_entry.pack(padx=10, pady=5, side=tk.LEFT)

        # Configuration du bouton pour rejoindre un salon
        self.join_button = tk.Button(self.root, text="Rejoindre salon", command=self.join_room)
        self.join_button.pack(padx=10, pady=5, side=tk.RIGHT)

        # Gestion de la fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_nickname(self, callback):
        nickname = simpledialog.askstring("Pseudo", "Choisissez un pseudo:", parent=self.root)
        callback(nickname)

    def setup_main_window(self):
        self.root.title(f"Chat - {self.controller.nickname}")
        self.root.geometry("400x500")

    def send_message(self):
        message = self.msg_entry.get()
        if message.strip():  # Vérifie si le message n'est pas vide
            self.controller.send_message(message)
            self.msg_entry.delete(0, tk.END)

    def join_room(self):
        room = self.room_entry.get()
        if room.strip():  # Vérifie si le nom de salon n'est pas vide
            self.controller.join_room(room)
            self.room_entry.delete(0, tk.END)

    def update_chat(self, message, is_own_message=False):
        self.chat_area.config(state='normal')
        if is_own_message:
            self.chat_area.insert(tk.END, f"You: {message}\n", 'self_msg')
        else:
            self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

        # Définition du style pour les messages de l'utilisateur
        self.chat_area.tag_config('self_msg', foreground='blue', font=('Arial', 10, 'bold'))

    def on_closing(self):
        self.controller.disconnect()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
