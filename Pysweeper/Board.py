import random

class Board(object):
    """class for handling the playing field for the game"""

    def __init__(self, h, w, m_no):
        self.height = h
        self.width = w
        self.mine_no = m_no
        self.filled_board = [["0" for col in range(self.height)] for row in range(self.width)]
        self.player_board = [[" " for col in range(self.height)] for row in range(self.width)]

    def genBoard(self, x, y):
        placed = []
        for m in range(self.mine_no):
            new_x = random.randint(0,self.width-1)
            new_y = random.randint(0,self.height-1)
            while [new_x, new_y] in placed:
                new_x = random.randint(0,self.width-1)
                new_y = random.randint(0,self.height-1)
            placed.append([new_x, new_y])
            self.filled_board[new_x][new_y] = "*" 
            #increase neighbor values
            neighbors = [[new_x-1, new_y-1],[new_x-1, new_y],[new_x-1, new_y+1],
                         [new_x,   new_y-1],                 [new_x,   new_y+1],
                         [new_x+1, new_y-1],[new_x+1, new_y],[new_x+1, new_y+1]]

            for n in neighbors:
                if n[0] in range(self.width) and n[1] in range(self.height) and (self.filled_board[n[0]][n[1]] != "*"):
                    prev = int(self.filled_board[n[0]][n[1]])
                    self.filled_board[n[0]][n[1]] = str(prev+1)

    def printBoard(self):
        """Print the players view of the field to stdout"""
        static_row = "   " + ("--- "*self.width)+" "
        print()
        letters = "abcdefghijklmnopqrstuvwxyz"[:self.width]
        print("    " + ''.join(map(lambda x: x+"   ", letters)))
        for i in range(self.height):
            print(static_row)
            dynrow =  str(i) + " |"
            for j in range(self.width):
                dynrow += " " + self.player_board[j][i] + " |"
            print(dynrow)
        print(static_row)

    def printSolution(self):
        """Print the solution of the field to stdout"""
        static_row = "   " + ("--- "*self.width)+" "
        print()
        letters = "abcdefghijklmnopqrstuvwxyz"[:self.width]
        print("    " + ''.join(map(lambda x: x+"   ", letters)))
        for i in range(self.height):
            print(static_row)
            dynrow =  str(i) + " |"
            for j in range(self.width):
                dynrow += " " + self.filled_board[j][i] + " |"
            print(dynrow)
        print(static_row)

    def turnTile(self, x,y):
        if self.player_board[x][y] != " " :
            print("This tile has already been turned")
        elif self.filled_board[x][y] == "0":
            #turn all neighbors
            self.player_board[x][y] = "-"
            neighbors = [[x-1, y], [x, y-1], [x, y+1], [x+1, y]]
            for n in neighbors:
                if (n[0] in range(self.width)) and (n[1] in range(self.height)) and self.player_board[n[0]][n[1]] == " ":
                    self.turnTile(n[0],n[1])
        else:
            self.player_board[x][y] = self.filled_board[x][y]
        
    def flagTile(self, x,y):
        if self.player_board[x][y] != " " :
            print("This tile has already been turned")
        elif self.player_board[x][y] == "F":
             self.player_board[x][y] = " "
        else:
            self.player_board[x][y] = "F"