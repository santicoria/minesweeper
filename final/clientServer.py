import random
import os
import socket
import threading
import pickle
import asyncio
import argparse
import queue
import tkinter as tk
from tkinter import messagebox, scrolledtext
from multiprocessing import Queue, Process
import pyfiglet
from rich import print
from gameLogic import Board, Mine, Clear, FullClear



class MinesweeperGUI:
    def __init__(self, host, ipv, port, master):
        self.host = host
        self.port = port
        self.ipv = ipv
        if(self.ipv == 6):
            self.client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        elif(self.ipv == 4):
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.client_socket.connect((self.host, self.port))
        self.go = False
        self.buttons = []
        self.master = master
        self.size = 0
        self.master.title("Minesweeper")
        
        self.receive_board()

        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]

        for x in range(self.size):
            for y in range(self.size):
                button = tk.Button(self.master, text='', width=3, height=1, command=lambda x=x, y=y: self.on_button_click(x, y))
                button.grid(row=x, column=y)
                self.buttons[x][y] = button

    # Registra los clicks en los botones y manda el comando correspondiente
    def on_button_click(self, x, y):
        print(f"Button clicked at ({x}, {y})")
        command = str(y) + " " + str(x)
        self.client_socket.send(command.encode('utf-8'))
        self.receive_board()

    # Recibe el tablero actualizado
    def receive_board(self):
        serialized_board = self.client_socket.recv(4096)
        board = pickle.loads(serialized_board)
        print(board.size_set)
        self.display_board(board)
        if(self.size == 0):
            self.size = board.size_set
    
    # Muestra el tablero
    def display_board(self, board):
        if(board.go == True):
            self.go = True
            title = pyfiglet.figlet_format('GAME OVER', font='cosmic')
            print(f'[red]{title}[/red]')
            self.master.destroy()
        else:
            print("Board updated:")
            for i in range(len(board.board)):
                for n in range(len(board.board[i])):
                    if(board.board[i][n][4]):
                        self.buttons[n][i].config(text=board.board[i][n][3])
        board.print_board(board.board)


class ChatClientApp:
    def __init__(self, host, port, ipv, root, user):
        self.root = root
        self.root.title("Cliente de Chat")
        self.host = host
        self.ipv = ipv
        self.port = port
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', width=50, height=15)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.tag_config('left', justify='left')
        self.chat_area.tag_config('right', justify='right')
        self.entry_message = tk.Entry(self.root, width=40)
        self.entry_message.pack(padx=10, pady=5, side=tk.LEFT)
        self.send_button = tk.Button(self.root, text="Enviar", command=self.send_message)
        self.send_button.pack(padx=10, pady=5, side=tk.LEFT)
        self.reader = None
        self.writer = None
        self.message_queue = queue.Queue()
        self.user = user
        
        # Crea el hilo que maneja la comunicacion del chat
        threading.Thread(target=self.start_asyncio_loop, daemon=True).start()

        self.root.after(100, self.check_new_messages)

    # Iniciar loop async
    def start_asyncio_loop(self):
        asyncio.run(self.connect_to_server())

    # Conectar al servidor de chat
    async def connect_to_server(self):
        if(self.ipv == 6):
            self.reader, self.writer = await asyncio.open_connection(self.host, int(self.port)+1, family=socket.AF_INET6)
        elif(self.ipv == 4):
            self.reader, self.writer = await asyncio.open_connection(self.host, int(self.port)+1)
        await self.receive_message()

    # Recibir mensaje y ponerlo en la cola
    async def receive_message(self):
        while True:
            data = await self.reader.read(100)
            if not data:
                break
            message = data.decode().strip()
            self.message_queue.put(message)

    # Chequea si hay mensajes nuevos en la cola. Si los hay, los muestra
    def check_new_messages(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, f"{message}\n")
            self.chat_area.yview(tk.END)
            self.chat_area.config(state='disabled')

        self.root.after(100, self.check_new_messages)

    # Manda los mensajes y muestra tu mensaje en tu chat
    def send_message(self):
        message = self.entry_message.get()
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, f"Tu:\n{message}\n", 'right')
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')
        if message and self.writer:
            full_message = f"{self.user}:\n{message}"
            self.writer.write(full_message.encode())
            asyncio.run_coroutine_threadsafe(self.writer.drain(), asyncio.get_event_loop())
            self.entry_message.delete(0, tk.END)
        


def parse_arguments():
    parser = argparse.ArgumentParser(description="Minesweeper Game Server/Client")
    parser.add_argument('--ipv', type=int, choices=[4, 6], default=0, help="Version de IP (4 o 6)")
    parser.add_argument('--host', type=str, default='127.0.0.1', help="Direccion IP del servidor")
    parser.add_argument('--port', type=int, default=5555, help="Puerto del servidor")
    parser.add_argument('--user', type=str, default='user', help="Tu nombre de usuario")
    return parser.parse_args()



if __name__ == "__main__":
    args = parse_arguments()

    chat_root = tk.Tk()
    root = tk.Tk()
    app = MinesweeperGUI(args.host, args.ipv, args.port, root)
    chat_app = ChatClientApp(args.host, args.port, args.ipv, chat_root, args.user)
    root.mainloop()
    chat_root.mainloop()