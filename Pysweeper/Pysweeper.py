import os
import re
import random

import Board

title = """
,------.,--.   ,--.,---. ,--.   ,--.,------.,------.,------. ,------.,------.  
|  .--. '\  `.'  /'   .-'|  |   |  ||  .---'|  .---'|  .--. '|  .---'|  .--. ' 
|  '--' | '.    / `.  `-.|  |.'.|  ||  `--, |  `--, |  '--' ||  `--, |  '--'.' 
|  | --'    |  |  .-'    |   ,'.   ||  `---.|  `---.|  | --' |  `---.|  |\  \  
`--'        `--'  `-----''--'   '--'`------'`------'`--'     `------'`--' '--' 
 """

def getParams():
    print(title)
    print("\t -The Game\n")
    try:
        print("Height:")
        inp = input("-> ")
        i = int(inp)
        if i < 1:
            os.system('CLS')
            print("Must be larger than 0")
            return [None, None, None]
        else:
            h = int(inp)

        print("Width:")
        inp = input("-> ")
        i = int(inp)
        if i < 1:
            os.system('CLS')
            print("Must be larger than 0")
            return [None, None, None]
        else:
            w = int(inp)

        print("Number of mines:")
        inp = input("-> ")
        i = int(inp)
        if 0 < i < (h*w-9):
            m_no = int(inp)
        else:
            os.system('CLS')
            print("Must be larger than 0 and smaller than the total number of squares minus 9")
            return [None, None, None]

        os.system('CLS')
        return [h, w, m_no]

    except ValueError:
        os.system('CLS')
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
        
    print(title)
    print("\t -The Game\n")

    #print("Generating board...", height, width, mine_no)
    print()
    field = Board.Board(height, width, mine_no)

    game_status = "running"
    first_move = True
    while game_status == "running":
        field.printBoard()
        try:
            print("Next move:")
            inp = input("-> ")
            os.system('CLS')
            print(title)
            print("\t -The Game\n")
            chars = re.findall("[a-zA-Z]+", inp)
            nums = re.findall("[0-9]+", inp)
            if chars[0].lower() == "exit":
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
        
        if game_status == "running_p":
            if not field.gameFinished():
                print("") #print empty line for consistency
            game_status = "running"

        if (field.gameFinished() and game_status == "running"):
            game_status = "won"

    if(game_status == "won"):
        print("Game won, gratiz!!")
    elif(game_status == "bombed"):
        print(random.choice(["OOOhh you got served bro!",
                             "You are LITTERALY the bomb! Well done!",
                             "You blew up.. does that make you feel any better about yourself?",
                             "You got your silly arse bombed"]))
    elif(game_status == "quitting"):
       print("Quitting game.. you quitter!")
       if first_move:
           field.genBoard(random.randint(0,width-1), random.randint(0,height-1))
    else:
        print("unexpected game endning:", game_status)
    field.flipBoard()
    field.printBoard()
    input("press enter")
    os.system('CLS')

def menu():
    while(True):
        print(title)
        print("\t -The Game\n")
        print("Please make your selection:\n")
        print("1: New Game")
        print("2: Options")
        print("3: Quit\n")
        inp = input("->")
        if inp == "1":
            os.system('CLS')
            run()
        elif inp == "2":
            os.system('CLS')
            print(title)
            print("\t -The Game\n")
            print("Nothing here.. yet")
            input("press enter")
            os.system('CLS')
        elif inp == "3":
            print("exiting")
            return
        else:
            os.system('CLS')
            print(title)
            print("\t -The Game\n")
            print("Invalid input!")
            input("press enter")
            os.system('CLS')

if __name__ == '__main__':
    menu()
    #run()