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

# Servidor del juego. Corre en un proceso. Se encarga de la logica de juego de cada partida y comunicar a 
# los clientes los movimientos
class GameServer:
    def __init__(self, host, port, ipv, difficulty):
        self.host = host
        self.port = port
        self.ipv = ipv
        self.difficulty = difficulty
        self.clients = {}
        self.board = Board(self.size_set())
        self.mine_list = self.mine_builder()
        if(self.ipv == 6):
            self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        elif (self.ipv == 4):
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define la cantidad de minas segun la dificultad elegida
    def mines_set(self):
        if (self.difficulty == 0):
            return 10
        elif (self.difficulty == 1):
            return 40
        elif (self.difficulty == 2):
            return 99

    # Define el tamaño del tablero segun la dificultad elegida
    def size_set(self):
        if (self.difficulty == 0):
            return 9
        elif (self.difficulty == 1):
            return 16
        elif (self.difficulty == 2):
            return 24

    # Crea las minas
    def mine_builder(self):
        mine_list = []

        mine_number = self.mines_set()

        for mine in range(mine_number):
            mine_pos_x = random.randrange(0, self.size_set(), 1)
            mine_pos_y = random.randrange(0, self.size_set(), 1)

            while ((mine_pos_x, mine_pos_y) in mine_list):
                mine_pos_x = random.randrange(0, self.size_set(), 1)
                mine_pos_y = random.randrange(0, self.size_set(), 1)
            
            mine_list.append((mine_pos_x, mine_pos_y))

        return mine_list
    
    # Chequea los alrededores
    def check_neighbours(self, board, x, y, mine_list, max_size):

        if(board.board[x][y][4] == 0):
            board.board[x][y][4] = 1

            if (board.board[x][y][3] == 0):
                if (x != 0):                                   #Check Norte
                    self.check_neighbours(board, x-1, y, mine_list, max_size)
                if (y != 0):                                   #Check Oeste
                    self.check_neighbours(board, x, y-1, mine_list, max_size)
                if (x != max_size-1):                          #Check Sur
                    self.check_neighbours(board, x+1, y, mine_list, max_size)
                if (y != max_size-1):                          #Check Este
                    self.check_neighbours(board, x, y+1, mine_list, max_size)
                if (x != 0) & (y != 0):                      #Check Noroeste
                    self.check_neighbours(board, x-1, y-1, mine_list, max_size)
                if (x != 0) & (y != max_size-1):             #Check Noreste
                    self.check_neighbours(board, x-1, y+1, mine_list, max_size)
                if (x != max_size-1) & (y != max_size-1):    #Check Sureste
                    self.check_neighbours(board, x+1, y+1, mine_list, max_size)
                if (x != max_size-1) & (y != 0):             #Check Suroeste
                    self.check_neighbours(board, x+1, y-1, mine_list, max_size)

            if (board.board[x][y][3] != 0):
                board.board[x][y][4] = 1

    # Revela la posicion de las minas. Por ej. cuando el usuario pierde
    def reveal_mines(self, board, mine_list):
        for mine in mine_list:
            board.board[mine[0]][mine[1]][4] = 1
            self.clear()
        return board

    # Maneja la conexion de los clientes
    def handle_client(self, client_socket, address):
        print(f"[NEW CONNECTION] {address} connected.")

        board = Board(self.size_set())
        mine_list = self.mine_builder()
        board.create_board(mine_list, self.size_set())
        self.clients[client_socket] = board
        self.send_board(client_socket)

        while True:
            try:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                response = self.process_command(data, client_socket)
                self.send_board(client_socket)

            except ConnectionResetError:
                print(f"[DISCONNECTED] {address} has disconnected.")
                break

        del self.clients[client_socket]
        client_socket.close()

    # Procesa los comandos introducidos por los clientes
    def process_command(self, command, client_socket):
        board = self.clients[client_socket]
        x = int(command.split()[0])
        y = int(command.split()[1])

        if ((x,y) in board.mine_list):
                return self.end_game(board)
        else:
            if (board.board[x][y][3] > 0):
                board.board[x][y][4] = 1
            else:
                self.check_neighbours(board, x, y, board.mine_list, board.size_set)

        self.clear()

        return board
    
    # Finaliza el juego si las condiciones estan dadas (El usuario selecciono una mina)
    def end_game(self, board):
        board.go = True
        self.reveal_mines(board, board.mine_list)

    # Envia el nuevo tablero al usuario
    def send_board(self, client_socket):
        board = self.clients[client_socket]
        serialized_board = pickle.dumps(board)
        client_socket.send(serialized_board)

    # Inicia el server
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[LISTENING] Server listening on {self.host}:{self.port}")
        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

    def clear(self):
        None

# Inicia el servidor de juego
async def run_server(host, port, difficulty, ipv):
    server = GameServer(host, port, ipv, difficulty)
    server_process = Process(target=server.start)
    server_process.start()
    print(f"Server running at {host}:{port}")
    await asyncio.sleep(5) 

# Inicia el servidor de chat
async def chat_main(host, ipv, port):
    if (ipv == 6):
        server = await asyncio.start_server(handle_client_chat, host, (int(port)+1), family=socket.AF_INET6)
    elif (ipv == 4):
        server = await asyncio.start_server(handle_client_chat, host, (int(port)+1))
    
    print("Servidor de chat iniciado en " + host + ":" + str(int(port)+1))

    async with server:
        await server.serve_forever()

# Manejador de clientes en el chat
connected_clients = []
async def handle_client_chat(reader, writer):
    address = writer.get_extra_info('peername')
    print(f"Cliente conectado: {address}")
    connected_clients.append(writer)

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break

            message = data.decode().strip()
            print(f"Mensaje de {address}: {message}")
            print(len(connected_clients))

            for client in connected_clients:
                if client != writer:
                    client.write(f"{message}\n".encode())
                    await client.drain()

    except ConnectionResetError:
        print(f"Cliente desconectado: {address}")

    finally:
        connected_clients.remove(writer)
        writer.close()
        await writer.wait_closed()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Minesweeper Game Server/Client")
    parser.add_argument('--ipv', type=int, choices=[4, 6], default=0, help="Version de IP (4 o 6)")
    parser.add_argument('--host', type=str, default='127.0.0.1', help="Direccion IP del servidor")
    parser.add_argument('--port', type=int, default=5555, help="Puerto del servidor")
    parser.add_argument('--difficulty', type=int, choices=[0, 1, 2], default=0, help="Dificultad de juego (0: Facil, 1: Medio, 2: Dificil)")
    return parser.parse_args()



if __name__ == "__main__":
    args = parse_arguments()

    asyncio.run(run_server(args.host, args.port, args.difficulty, args.ipv))
    asyncio.run(chat_main(args.host, args.ipv, args.port))