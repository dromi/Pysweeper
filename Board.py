import random

import util

class Board(object):
    """class for handling the playing field for the game"""
    

    def __init__(self, h, w, m_no):
        self.height = h
        self.width = w
        self.mine_no = m_no
        self.filled_board = [["0" for col in range(self.height)] for row in range(self.width)]
        self.player_board = [[" " for col in range(self.height)] for row in range(self.width)]
        self.empty = True

    def genBoard(self, x, y):
        self.empty = False        
        placed = []
        # Make sure quadrant surrounding first move is free
        sacred = [[x-1, y-1],[x-1, y],[x-1, y+1],
                  [x,   y-1],[x,   y],[x,   y+1],
                  [x+1, y-1],[x+1, y],[x+1, y+1]]
        for m in range(self.mine_no):
            new_x = random.randint(0,self.width-1)
            new_y = random.randint(0,self.height-1)
            while [new_x, new_y] in placed or [new_x, new_y] in sacred:
                new_x = random.randint(0,self.width-1)
                new_y = random.randint(0,self.height-1)
            placed.append([new_x, new_y])
            self.filled_board[new_x][new_y] = "*" 
            #increase neighbor values
            neighbors = [[new_x-1, new_y-1],[new_x-1, new_y],[new_x-1, new_y+1],
                         [new_x,   new_y-1],                 [new_x,   new_y+1],
                         [new_x+1, new_y-1],[new_x+1, new_y],[new_x+1, new_y+1]]

            for n in neighbors:
                if (0 <= n[0] < self.width) and (0 <= n[1] < self.height) and (self.filled_board[n[0]][n[1]] != "*"):
                    #NOTE: I could change it such that numbers are stored as numbers and bombs are chars
                    old_val = int(self.filled_board[n[0]][n[1]])
                    self.filled_board[n[0]][n[1]] = str(old_val+1)

    def getBoard(self):
        """Returns the players view of the field"""
        view = ""
        static_row = "  " + util.colorize((" "+"--- "*self.width),"grey","white") + " \n"

        if(self.width <= 10):
            view += ("    " + ''.join(map(lambda x: str(x)+"   ", range(self.width))) + "\n")
        else:
            view += "    " + ''.join(map(lambda x: str(x)+"   ", range(10)))[:-1]
            view += ''.join(map(lambda x: str(x)+"  ", range(10,self.width)))
            view += "\n"
        letters = "abcdefghijklmnopqrstuvwxyz"[:self.height]
        for i in range(self.height):
            view += static_row
            dyn_row = ""
            dyn_row += letters[i] + " " + util.colorize("|","grey","white")
            for j in range(self.width):
                dyn_row += util.colorByContent(self.player_board[j][i]) + util.colorize("|","grey","white")
            view += dyn_row + "\n"
        view += static_row
        return view

    def turnTile(self, x,y):
        if self.player_board[x][y] == "F": # turned a flag
            print("This tile has been flagged")
            return "running"
        elif self.filled_board[x][y] == "*":  # turned a mine
            self.player_board[x][y] = "X"
            return "bombed"
        elif self.filled_board[x][y] == "0": # turned a tile with 0 neighboring bombs
            #turn all neighbors
            self.player_board[x][y] = "-"
            neighbors = [[x-1, y-1],[x-1, y],[x-1, y+1],
                         [x,   y-1],         [x,   y+1],
                         [x+1, y-1],[x+1, y],[x+1, y+1]]

            for n in neighbors:
                if (n[0] in range(self.width)) and (n[1] in range(self.height)) and self.player_board[n[0]][n[1]] == " ":
                    self.turnTile(n[0],n[1])
            if self.gameFinished():
                return "won"
            else:
                return "running"
        elif self.player_board[x][y] != " " : # turned a tile that has already been turned
            print("This tile has already been turned")
            return "running"
        else: # turned a normal tile
            self.player_board[x][y] = self.filled_board[x][y]
            if self.gameFinished():
                return "won"
            else:
                return "running"
        
    def flagTile(self, x,y):
        if self.player_board[x][y] == "F":
            print(" ") #print empty line for consistency
            self.player_board[x][y] = " "
        elif self.player_board[x][y] == " " :
            print(" ") #print empty line for consistency
            self.player_board[x][y] = "F"
        else:
            print("This tile has already been turned")

    def gameFinished(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.player_board[i][j] in ["F"," "] and self.filled_board[i][j] != "*":
                    return False
        return True

    def flipBoard(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.player_board[i][j] == " " and self.filled_board[i][j] == "*":
                    self.player_board[i][j] = "*"
                if self.player_board[i][j] == "F" and not self.filled_board[i][j] == "*":
                    self.player_board[i][j] = "U"
