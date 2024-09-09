import random
import os
import socket
import threading
import pickle
import asyncio
import argparse
import tkinter as tk
from tkinter import messagebox
from multiprocessing import Queue, Process
import pyfiglet
from rich import print


class Board():

    def __init__(self, size_set):
        self.size_set = size_set
        self.board = []
        self.mine_list = []
        self.go = False


    def create_board(self, mine_list, rows_len):
        self.mine_list = mine_list
        rows = []

        for x in range(rows_len):
            row = []
            for y in range(rows_len):
                row.append(self.check_if_clear(x, y,rows_len, mine_list))
            rows.append(row)
        # self.print_board(rows)
        self.board = rows
        return self.board
    
    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value
    
    def print_board(self, rows):

        n = self.size_set
        print()
        print("\t\t\tMINESWEEPER\n")
    
        st = "   "
        for i in range(n):
            st = st + "     " + str(i)
        print(st)   
    
        for r in range(n):
            st = "     "
            if r == 0:
                for col in range(n):
                    st = st + "______" 
                print(st)
    
            st = "     "
            for col in range(n):
                st = st + "|     "
            print(st + "|")
            
            st = "  " + str(r) + "  "
            for col in range(n):
                if ((rows[col][r][4]) == 1) & (rows[col][r][2] == "Mina"):
                    st = st + "|  " + "M" + "  "
                elif ((rows[col][r][4]) == 1) & (rows[col][r][2] == "Clear"):
                    st = st + "|  " + str(rows[col][r][3]) + "  "
                elif ((rows[col][r][4]) == 1) & (rows[col][r][2] == "Full Clear"):
                    st = st + "|  " + str(rows[col][r][3]) + "  "
                elif ((rows[col][r][4]) == 0):
                    st = st + "|  " + "-" + "  "

            print(st + "|") 
    
            st = "     "
            for col in range(n):
                st = st + "|_____"
            print(st + '|')
    
        print()

    def check_if_clear(self, x, y, max_size, mine_list):
        if ((x,y) in mine_list):
            return [x, y, Mine().tipo(), 0, 0]
        
        else:
            counter = 0
            if (x != 0) & ((x-1,y) in mine_list):                                   #Check Norte
                counter += 1
            if (y != 0) & ((x,y-1) in mine_list):                                   #Check Oeste
                counter += 1
            if (x != max_size-1) & ((x+1,y) in mine_list):                          #Check Sur
                counter += 1
            if (y != max_size-1) & ((x,y+1) in mine_list):                          #Check Este
                counter += 1
            if (x != 0) & (y != 0) & ((x-1,y-1) in mine_list):                      #Check Noroeste
                counter += 1
            if (x != 0) & (y != max_size-1) & ((x-1,y+1) in mine_list):             #Check Noreste
                counter += 1
            if (x != max_size-1) & (y != max_size-1) & ((x+1,y+1) in mine_list):    #Check Sureste
                counter += 1
            if (x != max_size-1) & (y != 0) & ((x+1,y-1) in mine_list):             #Check Suroeste
                counter += 1
            
            if (counter == 0):
                return [x, y, FullClear().tipo(), 0, 0]
            elif (counter != 0):
                return [x, y, Clear().tipo(), counter, 0]
            
    def game_over(self):
        self.go = True

class Mine():
    
    def tipo(self):
        return "Mina"

class Clear():

    def tipo(self):
        return "Clear"


class FullClear():

    def tipo(self):
        return "Full Clear"


class GameServer:
    def __init__(self, host, port, difficulty):
        self.host = host
        self.port = port
        self.difficulty = difficulty
        self.clients = {}
        self.board = Board(self.size_set())
        self.mine_list = self.mine_builder()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def mines_set(self):
        if (self.difficulty == 0):
            return 10
        elif (self.difficulty == 1):
            return 40
        elif (self.difficulty == 2):
            return 99

    def size_set(self):
        if (self.difficulty == 0):
            return 9
        elif (self.difficulty == 1):
            return 16
        elif (self.difficulty == 2):
            return 24

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

    def reveal_mines(self, board, mine_list):
        for mine in mine_list:
            board.board[mine[0]][mine[1]][4] = 1
            self.clear()
        return board

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
    
    def end_game(self, board):
        board.go = True
        self.reveal_mines(board, board.mine_list)

    
    def send_board(self, client_socket):
        board = self.clients[client_socket]
        serialized_board = pickle.dumps(board)
        client_socket.send(serialized_board)

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


class MinesweeperGUI:
    def __init__(self, host, port, master):
        self.host = host
        self.port = port
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

    def on_button_click(self, x, y):
        print(f"Button clicked at ({x}, {y})")
        command = str(y) + " " + str(x)
        self.client_socket.send(command.encode('utf-8'))
        self.receive_board()

    def receive_board(self):
        serialized_board = self.client_socket.recv(4096)
        board = pickle.loads(serialized_board)
        print(board.size_set)
        self.display_board(board)
        if(self.size == 0):
            self.size = board.size_set
    
    def display_board(self, board):
        print(board.board)
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
        

async def run_server(host, port, difficulty):
    server = GameServer(host, port, difficulty)
    server_process = Process(target=server.start)
    server_process.start()
    print(f"Server running at {host}:{port}")
    await asyncio.sleep(5) 


def parse_arguments():
    parser = argparse.ArgumentParser(description="Minesweeper Game Server/Client")
    parser.add_argument('--mode', choices=['server', 'client'], required=True, help="Run as server or client")
    parser.add_argument('--host', type=str, default='127.0.0.1', help="Server IP address")
    parser.add_argument('--port', type=int, default=5555, help="Server port")
    parser.add_argument('--difficulty', type=int, choices=[0, 1, 2], default=0, help="Game difficulty (0: Easy, 1: Medium, 2: Hard)")
    return parser.parse_args()

def gui_main(size):
    root = tk.Tk()
    app = MinesweeperGUI(root, size)
    root.mainloop()

if __name__ == "__main__":
    args = parse_arguments()

    if args.mode == 'server':
        asyncio.run(run_server(args.host, args.port, args.difficulty))
    elif args.mode == 'client':
        root = tk.Tk()
        app = MinesweeperGUI(args.host, args.port, root)
        root.mainloop()