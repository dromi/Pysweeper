import random
import sys

width = 1
height = 1
mine_no = 0

filled_board = []
player_board = []

def printBoard():
    static_row = "   " + ("--- "*width)+" "
    print()
    letters = "abcdefghijklmnopqrstuvwxyz"[:width]
    print("    " + ''.join(map(lambda x: x+"   ", letters)))
    for i in range(height):
        print(static_row)
        dynrow =  str(i) + " |"
        for j in range(width):
            dynrow += " " + filled_board[j][i] + " |"
        print(dynrow)
    print(static_row)

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

def run():
    # Get input for size and no of mines
    try:
        print("Height:")
        inp = input("-> ")
        i = int(inp)
        if i < 1:
            print("Must be larger than 0")
            return
        else:
            global height
            height = int(inp)
    except ValueError:
        print("Could not convert data to an integer.")
        return

    try:
        print("Width:")
        inp = input("-> ")
        i = int(inp)
        if i < 1:
            print("Must be larger than 0")
            return
        else:
            global width
            width = int(inp)
    except ValueError:
        print("Could not convert data to an integer.")
        return

    try:
        print("Number of mines:")
        inp = input("-> ")
        i = int(inp)
        if 0 < i < (height*width):
            global mine_no
            mine_no = int(inp)
        else:
            print("Must be larger than 0 and smaller than the total number of squares")
            return
    except ValueError:
        print("Could not convert data to an integer.")
        return

    print("Generating board...", height, width, mine_no)
    genBoard()
    printBoard()


if __name__ == '__main__':
    run()