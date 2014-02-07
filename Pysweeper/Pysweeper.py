import os
import re
import random
import platform

import Board

title_text = """
,------.,--.   ,--.,---. ,--.   ,--.,------.,------.,------. ,------.,------.  
|  .--. '\  `.'  /'   .-'|  |   |  ||  .---'|  .---'|  .--. '|  .---'|  .--. ' 
|  '--' | '.    / `.  `-.|  |.'.|  ||  `--, |  `--, |  '--' ||  `--, |  '--'.' 
|  | --'    |  |  .-'    |   ,'.   ||  `---.|  `---.|  | --' |  `---.|  |\  \  
`--'        `--'  `-----''--'   '--'`------'`------'`--'     `------'`--' '--' 

\t -The Game\n
 """

clear_cmd = ''

max_height = 30
max_width = 26

def findOS():
     global clear_cmd 
     if platform.system() == 'Windows':
         clear_cmd = 'CLS'
     elif platform.system() == 'Linux':
         clear_cmd = 'clear'

def title():
    os.system(clear_cmd)
    print(title_text)



def help():
    print("""Pysweeper. Like Minesweeper you know?..

 - : Empty spot with no adjecent mines
1-8: Indicates number of adjacent mines
 F : Flagged spot
 U : Wrongly placed flag
 * : Mine
 X : Exploded mine
    """)
    input("press enter")

def options():
    print("Graphical settings:\n")
    print("1: ASCII           <---")
    print("2: Fancy Fancy GUI")
    inp = input("->")
    if inp == "1":
        title()
        print("Good choice!\n")
        input("press enter")
    elif inp == "2":
        title()
        print("ERROR Only ASCII graphics avaliable (this is after all an ASCII game..)\n")
        input("press enter")
    else:
        title()
        print("ERROR! Bad input. No optioning for you\n")
        input("press enter")



def getParams():
    print("Input game parameters\n")

    height = None
    width = None
    mine_no = None

    while(height == None):
        try:
            print("Height:")
            inp = input("-> ")
            i = int(inp)
            if i < 1:
                print("Must be larger than 0")
            elif i > max_height:
                print("Must be smaller than",max_height)
            else:
                height = int(inp)
        except ValueError:
            print("Could not convert data to an integer")

    while(width == None):
        try:
            print("Width:")
            inp = input("-> ")
            i = int(inp)
            if i < 1:
                print("Must be larger than 0")
            elif i > max_width:
                print("Must be smaller than",max_width)
            else:
                width = int(inp)
        except ValueError:
            print("Could not convert data to an integer")

    while(mine_no == None):
        try:
            print("Number of mines:")
            inp = input("-> ")
            i = int(inp)
            if i < 1:
                print("Must be larger than 0")
            elif i > (height*width-9):
                print("Must be smaller than",(height*width-9), "(total number of squares minus 9)")
            else:
                mine_no = int(inp)
        except ValueError:
            print("Could not convert data to an integer")

    return [height, width, mine_no]


def run():
    """Run the game"""
    # Get input for size and no of mines

    [height, width, mine_no] = getParams()

    """
    8 lines title
    3 lines spacing and info
    1 line letters
    2 lines pr row
    1 row final
    2 lines user input
    ==
    14 + 2*rows
    """
    os.system("mode con lines=" + str(18+2*height)) #resize cmd window to fit field

    """
    3 numbers
    4 pr col
    1 final
    4 for symetry
    ==
    4 + 4*cols
    """

    if width > 18:
        os.system("mode con cols=" + str(7+4*width)) #resize cmd window to fit field
    else:
        os.system("mode con cols=80") #resize cmd window to default size

    title()
    #print("Generating board...", height, width, mine_no)
    print() #print empty line for consistency
    field = Board.Board(height, width, mine_no)

    game_status = "running"
    first_move = True
    while game_status == "running":
        field.printBoard()
        try:
            print("\nNext move:")
            inp = input("-> ")
            title()
            chars = re.findall("[a-zA-Z]+", inp)
            nums = re.findall("[0-9]+", inp)
            if chars[0].lower() in ["exit","quit"]:
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
        print("Game won, gratz!!")
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
    os.system(clear_cmd)

def menu():
    while(True):
        title()
        print("Please make your selection:\n")
        print("1: New Game")
        print("2: Options")
        print("3: Help")
        print("4: Quit\n")
        inp = input("->")
        title()
        if inp == "1":
            run()
        elif inp == "2":
            options()
        elif inp == "3":
            help()
        elif inp == "4":
            print("exiting\n")
            return
        else:
            print("Invalid input!\n")
            input("press enter")

if __name__ == '__main__':
    #os.system("mode con lines=30") #resize cmd window
    findOS()
    menu()
    #run()