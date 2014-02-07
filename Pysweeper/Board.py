import random
from colorama import Back, init, Fore

class Board(object):
    """class for handling the playing field for the game"""
    

    def __init__(self, h, w, m_no):
        self.height = h
        self.width = w
        self.mine_no = m_no
        self.filled_board = [["0" for col in range(self.height)] for row in range(self.width)]
        self.player_board = [[" " for col in range(self.height)] for row in range(self.width)]
        init() #initialize colorama

    def genBoard(self, x, y):
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
                if n[0] in range(self.width) and n[1] in range(self.height) and (self.filled_board[n[0]][n[1]] != "*"):
                    prev = int(self.filled_board[n[0]][n[1]])
                    self.filled_board[n[0]][n[1]] = str(prev+1)

    def printBoard(self):
        """Print the players view of the field to stdout"""
        static_row = "   " + Back.WHITE + Fore.BLACK + " " + ("--- "*self.width) + Back.RESET + Fore.RESET + " "
        print()
        letters = "abcdefghijklmnopqrstuvwxyz"[:self.width]
        print("     " + ''.join(map(lambda x: x+"   ", letters)))
        for i in range(self.height):
            print(static_row)
            dyn_row = ""
            if i < 10:
                dyn_row +=  " "
            dyn_row += str(i) + " " + Back.WHITE + Fore.BLACK +  "|" + Back.RESET + Fore.RESET
            for j in range(self.width):
                dyn_row += " " + self.player_board[j][i] + " " + Back.WHITE + Fore.BLACK + "|" + Back.RESET + Fore.RESET
            print(dyn_row)
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
            return "running_p"
        elif self.player_board[x][y] != " " :
            print("This tile has already been turned")
            return "running"
        else:
            self.player_board[x][y] = self.filled_board[x][y]
            return "running_p"
        
    def flagTile(self, x,y):
        if self.player_board[x][y] == "F":
            print(" ") #print empty line for consistency
            self.player_board[x][y] = " "
        elif self.player_board[x][y] != " " :
            print("This tile has already been turned")
        else:
            print(" ") #print empty line for consistency
            self.player_board[x][y] = "F"

    def gameFinished(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.player_board[i][j] == "F" and self.filled_board[i][j] != "*":
                    return False
                elif self.player_board[i][j] == " " and self.filled_board[i][j] != "*":
                    return False
        return True

    def flipBoard(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.player_board[i][j] == " " and self.filled_board[i][j] == "*":
                    self.player_board[i][j] = "*"
                if self.player_board[i][j] == "F" and not self.filled_board[i][j] == "*":
                    self.player_board[i][j] = "U"

