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