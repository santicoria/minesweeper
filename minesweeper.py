import random
import os

class Board():

    def __init__(self, size_set):
        self.size_set = size_set
        self.board = []

    def create_board(self, mine_list, rows_len):
        rows = []

        for x in range(rows_len):
            row = []
            for y in range(rows_len):
                row.append(self.check_if_clear(x, y,rows_len, mine_list))
            rows.append(row)
        self.print_board(rows)
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

class Mine():
    
    def tipo(self):
        return "Mina"

class Clear():

    def tipo(self):
        return "Clear"


class FullClear():

    def tipo(self):
        return "Full Clear"
    

class Game():
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.board = Board(self.size_set())

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
            

    def check_neighbours(self, x, y, mine_list, max_size):

        if(self.board.board[x][y][4] == 0):
            self.board.board[x][y][4] = 1

            if (self.board.board[x][y][3] == 0):
                if (x != 0):                                   #Check Norte
                    self.check_neighbours(x-1, y, mine_list, max_size)
                if (y != 0):                                   #Check Oeste
                    self.check_neighbours(x, y-1, mine_list, max_size)
                if (x != max_size-1):                          #Check Sur
                    self.check_neighbours(x+1, y, mine_list, max_size)
                if (y != max_size-1):                          #Check Este
                    self.check_neighbours(x, y+1, mine_list, max_size)
                if (x != 0) & (y != 0):                      #Check Noroeste
                    self.check_neighbours(x-1, y-1, mine_list, max_size)
                if (x != 0) & (y != max_size-1):             #Check Noreste
                    self.check_neighbours(x-1, y+1, mine_list, max_size)
                if (x != max_size-1) & (y != max_size-1):    #Check Sureste
                    self.check_neighbours(x+1, y+1, mine_list, max_size)
                if (x != max_size-1) & (y != 0):             #Check Suroeste
                    self.check_neighbours(x+1, y-1, mine_list, max_size)

            if (self.board.board[x][y][3] != 0):
                self.board.board[x][y][4] = 1

    
    def reveal_mines(self, board, mine_list):
        for mine in mine_list:
            board[mine[0]][mine[1]][4] = 1
            self.clear()
        self.board.print_board(board)
    
    def play(self):

        mine_list = self.mine_builder()
        rows_len = self.size_set()

        playable = True
        board = self.board.create_board(mine_list, rows_len)

        while playable:
            cell = input("Choose cell (ex: 2 2): ")
            x = int(cell.split()[0])
            y = int(cell.split()[1])

            if ((x,y) in mine_list):
                playable = False
            else:
                if (board[x][y][3] > 0):
                    self.board.board[x][y][4] = 1
                else:
                    self.check_neighbours(x, y, mine_list, rows_len)

            self.clear()
            self.board.print_board(board)
        self.reveal_mines(board, mine_list)
        print("\t\t\tGAME OVER\n")

    def clear(self):
        os.system("clear")


if __name__ == "__main__":
    dificultad = input("Seleccione la dificultad:\nFacil (9x9): 0\nMedio (16x16): 1\nDificil (24x24): 2\n----> ")
    game = Game(int(dificultad))

    play_game = game.play()
