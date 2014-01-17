import sys
import re

import Board

def getParams():
    try:
        print("Height:")
        inp = input("-> ")
        i = int(inp)
        if i < 1:
            print("Must be larger than 0")
            return [None, None, None]
        else:
            h = int(inp)

        print("Width:")
        inp = input("-> ")
        i = int(inp)
        if i < 1:
            print("Must be larger than 0")
            return [None, None, None]
        else:
            w = int(inp)

        print("Number of mines:")
        inp = input("-> ")
        i = int(inp)
        if 0 < i < (h*w):
            m_no = int(inp)
        else:
            print("Must be larger than 0 and smaller than the total number of squares")
            return [None, None, None]

        return [h, w, m_no]

    except ValueError:
        print("Could not convert data to an integer.")
        return [None, None, None]

def run():
    """Run the game"""
    # Get input for size and no of mines
    width = None
    height = None
    mine_no = None

    while height == None:
        [height, width, mine_no] = getParams()
        
    print("Generating board...", height, width, mine_no)
    field = Board.Board(height, width, mine_no)

    game_status = "running"
    first_move = True
    while game_status == "running":
        field.printBoard()
        try:
            print("Next move:")
            inp = input("-> ")
            chars = re.findall("[a-zA-Z]+", inp)
            nums = re.findall("[0-9]+", inp)
            if chars[0].lower() == "exit":
                print("Quitting Pysweeper")
                game_status = "quitting"
            elif chars[0].lower() == "flag" and len(nums) == 1 and len(chars) == 2 and chars[1] in "abcdefghijklmnopqrstuvwxyz"[:width] and int(nums[0]) in range(height):
                if first_move:
                    print("Can't flag on first turn")
                else:
                    x = "abcdefghijklmnopqrstuvwxyz".index(chars[1])
                    y = int(nums[0])
                    field.flagTile(x,y)
            elif (len(nums) == len(chars) == 1) and chars[0] in "abcdefghijklmnopqrstuvwxyz"[:width] and int(nums[0]) in range(height):
                x = "abcdefghijklmnopqrstuvwxyz".index(chars[0])
                y = int(nums[0])
                if first_move:
                    field.genBoard(x,y)
                    first_move = False
                game_status = field.turnTile(x,y)
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")
        except IndexError:
            print("Invalid input")

        if (field.gameFinished() and game_status == "running"):
            game_status = "won"

    print("Game ended with status " + game_status)

if __name__ == '__main__':
    run()