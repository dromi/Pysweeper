import random

width = 15
height = 7

mine_no = 10

filled_board = []
player_board = []

statrow = "   " + ("--- "*width)+" "

def printBoard():
    print()
    letters = "abcdefghijklmnopqrstuvwxyz"[:width]
    print("    " + ''.join(map(lambda x: x+"   ", letters)))
    for i in range(height):
        print(statrow)
        dynrow =  str(i) + " |"
        for j in range(width):
            dynrow += " " + filled_board[j][i] + " |"
        print(dynrow)
    print(statrow)

def genBoard():
    placed = []
    temp_board = [["0" for col in range(height)] for row in range(width)]
    player_board[:] = temp_board
    for m in range(mine_no):
        new_x = random.randint(0,width-1)
        new_y = random.randint(0,height-1)
        while [new_x, new_y] in placed:
            new_x = random.randint(0,width-1)
            new_y = random.randint(0,height-1)
        placed.append([new_x, new_y])
        temp_board[new_x][new_y] = "*" 
        #increase neighbor values
        neighbors = [[new_x-1, new_y-1],[new_x-1, new_y],[new_x-1, new_y+1],
                     [new_x,   new_y-1],                 [new_x,   new_y+1],
                     [new_x+1, new_y-1],[new_x+1, new_y],[new_x+1, new_y+1]]

        for n in neighbors:
            if (0 <= n[0] < width) and (0 <= n[1] < height) and (temp_board[n[0]][n[1]] != "*"):
                prev = int(temp_board[n[0]][n[1]])
                temp_board[n[0]][n[1]] = str(prev+1)
    filled_board[:] = temp_board

genBoard()
printBoard()


