#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import random
import platform

import Board
import ASCIIPrinter

logo = """
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

alphabet = "abcdefghijklmnopqrstuvwxyz"

def findOS():
    global clear_cmd 
    if platform.system() == 'Windows':
        clear_cmd = 'CLS'
    elif platform.system() == 'Linux':
        clear_cmd = 'clear'

def title():
    os.system(clear_cmd)
    print(logo)


def help():
    p.pushToBody("""\
Pysweeper. Like Minesweeper you know?..

  - : Empty spot with no adjecent mines
 1-8: Indicates number of adjacent mines
  F : Flagged spot
  U : Wrongly placed flag
  * : Mine
  X : Exploded mine\
""")
    p.flush()
    p.getUserConfirm()

def options():
    p.setMsg("Options:")
    p.pushToBody("Graphical settings:\n")
    p.pushToBody("1: ASCII              <---")
    p.pushToBody("2: Fancy Fancy GUI")
    p.flush()
    inp = p.getUserInput()
    if inp == "1":
        p.pushToBody("Good choice!\n")
        p.flush()
        p.getUserConfirm()
    elif inp == "2":
        p.pushToBody("ERROR Only ASCII graphics avaliable (this is after all an ASCII game..)\n")
        p.flush()
        p.getUserConfirm()
    else:
        p.pushToBody("ERROR! Bad input. No optioning for you\n")
        p.flush()
        p.getUserConfirm()

def getParams():
    p.setMsg("Input game parameters")

    height = None
    width = None
    mine_no = None

    while(height == None):
        try:
            p.pushToBody("Height:")
            p.flush()
            inp = p.getUserInput()
            i = int(inp)
            if (0 < i < max_height):
                height = int(inp)
            else:
                p.pushToBody("ERROR: Height must be between 1 and " + str(max_height) + "\n")
        except ValueError:
            p.pushToBody("ERROR: Could not convert data to an integer\n")

    while(width == None):
        try:
            p.pushToBody("Width:")
            p.flush()
            inp = p.getUserInput()
            i = int(inp)
            if (0 < i < max_width):
                width = int(inp)
            else:
                p.pushToBody("ERROR: Width must be between 1 and " + str(max_width) + "\n")
        except ValueError:
            p.pushToBody("ERROR: Could not convert data to an integer\n")

    while(mine_no == None):
        try:
            p.pushToBody("Number of mines:")
            p.flush()
            inp = p.getUserInput()
            i = int(inp)
            if (0 < i < (height*width-9)):
                mine_no = int(inp)
            else:
                p.pushToBody("ERROR: Number of mines must be between 1 and " + str(height*width-9) + "\n")
        except ValueError:
            p.pushToBody("ERROR: Could not convert data to an integer\n")

    return [height, width, mine_no]

def run():
    """Run the main game loop"""
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
    # os.system("mode con lines=" + str(18+2*height)) #resize cmd window to fit field

    """
    3 numbers
    4 pr col
    1 final
    4 for symetry
    ==
    4 + 4*cols
    """

    # if width > 18:
    #     os.system("mode con cols=" + str(7+4*width)) #resize cmd window to fit field
    # else:
    #     os.system("mode con cols=80") #resize cmd window to default size

    title()
    #print("Generating board...", height, width, mine_no)
    print() #print empty line for consistency
    field = Board.Board(height, width, mine_no)

    game_status = "first_move"
    while game_status in ["running","first_move"]:
        field.printBoard()
        try:
            print("\n gamestatus:",game_status)
            print("\nNext move:")
            inp = input("-> ")
            title()
            chars = re.findall("[a-zA-Z]+", inp)
            nums = re.findall("[0-9]+", inp)
            if chars[0].lower() in ["exit","quit"]:
                game_status = "quitting"
            elif chars[0].lower() == "flag":
               if game_status == "first_move":
                    raise IOError("Can't flag on first turn")
               if (len(nums) == 1 and len(chars) == 2 and chars[1] in alphabet[:width] and int(nums[0]) in range(height)):
                    x = alphabet.index(chars[1])
                    y = int(nums[0])
                    field.flagTile(x,y)
            elif ((len(nums) == len(chars) == 1) and chars[0] in alphabet[:width] and int(nums[0]) in range(height)):
                x = alphabet.index(chars[0])
                y = int(nums[0])
                if game_status == "first_move":
                    print("creating board")
                    field.genBoard(x,y)
                game_status = field.turnTile(x,y)
                print("current status:",game_status)
            else:
                 raise ValueError("Invalid or no input")
        except ValueError as e:
            print("ValueError occured:", e)
        except IndexError as e:
            print("IndexError occured:", e)
        except IOError as e:
            print("IOError occured:", e)
        
        # if game_status == "running_p":
        #     if not field.gameFinished():
        #         print("") #print empty line for consistency
        #     game_status = "running"

        # if (field.gameFinished() and game_status == "running"):
        #     game_status = "won"

    if(game_status == "won"):
        print("Game won, gratz!!")
    elif(game_status == "bombed"):
        print(random.choice(["OOOhh you got served bro!",
                             "You are LITTERALY the bomb! Well done!",
                             "You blew up.. does that make you feel any better about yourself?",
                             "You got your silly arse bombed"]))
    elif(game_status == "quitting"):
       print("Quitting game.. you quitter!")
       if game_status == "first_move":
           field.genBoard(random.randint(0,width-1), random.randint(0,height-1))
    else:
        print("unexpected game endning:", game_status)
    field.flipBoard()
    field.printBoard()
    input("press enter")
    os.system(clear_cmd)

def main_menu():
    while(True):
        p.setMsg("Please make your selection:")
        p.pushToBody("1: New Game")
        p.pushToBody("2: Options")
        p.pushToBody("3: Help")
        p.pushToBody("4: Quit")
        p.flush()
        inp = p.getUserInput()
        if inp == "1":
            run()
        elif inp == "2":
            options()
        elif inp == "3":
            help()
        elif inp == "4":
            p.pushToBody("Exiting..")
            p.flush()
            return
        else:
            p.pushToBody("Invalid input!")
            p.flush()
            p.getUserConfirm()

if __name__ == '__main__':
    #os.system("mode con lines=30") #resize cmd window
    findOS()
    p = ASCIIPrinter.ASCIIPrinter()
    main_menu()
    #run()
