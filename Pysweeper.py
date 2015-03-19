#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import random
import platform

import Board
import ASCIIPrinter
import Controller

max_height = 30
max_width = 26

alphabet = "abcdefghijklmnopqrstuvwxyz"

def help():
    view.setMsg("Help:")
    view.print("""\
Pysweeper. Like Minesweeper you know?..

  - : Empty spot with no adjecent mines
 1-8: Indicates number of adjacent mines
  F : Flagged spot
  U : Wrongly placed flag
  * : Mine
  X : Exploded mine\
""")
    view.getUserConfirm()

def options():
    view.setMsg("Options:")
    view.pushToBody("Graphical settings:\n")
    view.pushToBody("1: ASCII              <---")
    view.pushToBody("2: Fancy Fancy GUI")
    view.flush()
    inp = view.getUserInput()
    if inp == "1":
        view.print("Good choice!\n")
        view.getUserConfirm()
    elif inp == "2":
        view.print("ERROR Only ASCII graphics avaliable (this is after all an ASCII game..)\n")
        view.getUserConfirm()
    else:
        view.print("ERROR! Bad input. No optioning for you\n")
        view.getUserConfirm()

def main_menu():
    while(True):
        try:
            view.setMsg("Please make your selection:")
            view.pushToBody("1: New Game")
            view.pushToBody("2: Options")
            view.pushToBody("3: Help")
            view.pushToBody("4: Quit")
            view.flush()
            inp = view.getUserInput()
            i = int(inp)
            if i == 1:
                controller.setGameMode()
                controller.run()
            elif i == 2:
                options()
            elif i == 3:
                help()
            elif i == 4:
                view.print("Exiting..")
                return
            else:
                view.print("Invalid input!")
                view.getUserConfirm()
        except ValueError:
                view.print("Not a damn number")
                view.getUserConfirm()

if __name__ == '__main__':
    #os.system("mode con lines=30") #resize cmd window
    view = ASCIIPrinter.ASCIIPrinter()
    controller = Controller.Controller(view)
    main_menu()
