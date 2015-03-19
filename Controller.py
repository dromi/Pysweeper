import re
import random

import ASCIIPrinter
import Board

max_height = 25
max_width = 40

alphabet = "abcdefghijklmnopqrstuvwxyz"

class Controller(object):
    """Controller class for processing user inputs"""

    def __init__(self, ap):
        """initialize controller"""
        self.view = ap
        self.field = None
        self.height = None
        self.width = None
        self.mine_no = None
        self.game_status = "not_in_game"

    def reset(self):
        self.field = None
        self.height = None
        self.width = None
        self.mine_no = None
        self.game_status = "not_in_game"

    def setGameMode(self):
        """Set parameters for game mode"""
        while(not self.height):
            try:
                self.view.setMsg("Choose difficulty level:")
                self.view.pushToBody("1: Easy")
                self.view.pushToBody("2: Medium")
                self.view.pushToBody("3: Hard")
                self.view.pushToBody("4: Custom")
                self.view.flush()
                inp = self.view.getUserInput()
                i = int(inp)
                if i == 1:
                    self.height  = 9
                    self.width   = 9
                    self.mine_no = 10
                elif i == 2:
                    self.height  = 16
                    self.width   = 16
                    self.mine_no = 40
                elif i == 3:
                    self.height  = 16
                    self.width   = 30
                    self.mine_no = 99
                elif i == 4:
                    self.getCustomParams()
                else:
                    raise ValueError
            except ValueError:
                self.view.print("Invalid input!")
                self.view.getUserConfirm()


    def getCustomParams(self):
        """Set custom parameters for game mode"""
        self.view.setMsg("Input game parameters")

        while(not self.height):
            try:
                self.view.pushToBody("Height:")
                self.view.flush()
                inp = self.view.getUserInput()
                i = int(inp)
                if (0 < i <= max_height):
                    self.height = int(inp)
                else:
                    self.view.pushToBody("ERROR: Height must be between 1 and " + str(max_height) + "\n")
            except ValueError:
                self.view.pushToBody("ERROR: Could not convert data to an integer\n")
        
        while(not self.width):
            try:
                self.view.pushToBody("Width:")
                self.view.flush()
                inp = self.view.getUserInput()
                i = int(inp)
                if (0 < i <= max_width):
                    self.width = int(inp)
                else:
                    self.view.pushToBody("ERROR: Width must be between 1 and " + str(max_width) + "\n")
            except ValueError:
                self.view.pushToBody("ERROR: Could not convert data to an integer\n")

        while(not self.mine_no):
            try:
                self.view.pushToBody("Number of mines:")
                self.view.flush()
                inp = self.view.getUserInput()
                i = int(inp)
                if (0 < i <= (self.height*self.width-9)):
                    self.mine_no = int(inp)
                else:
                    self.view.pushToBody("ERROR: Number of mines must be between 1 and " + str(self.height*self.width-9) + "\n")
            except ValueError:
                self.view.pushToBody("ERROR: Could not convert data to an integer\n")


    def run(self):
        """Run the main game loop"""
        self.field = Board.Board(self.height, self.width, self.mine_no)

        self.game_status = "first_move"
        self.view.setMsg("Make your first move:")
        while self.game_status in ["running","first_move"]:
            self.view.print(self.field.getBoard())
            try:
                inp = self.view.getUserInput()
                chars = re.findall("[a-zA-Z]+", inp)
                nums = re.findall("[0-9]+", inp)
                if chars[0].lower() in ["exit","quit"]:
                    self.game_status = "quitting"
                elif chars[0].lower() == "flag":
                    if self.game_status == "first_move":
                        raise ValueError("Can't flag on first turn")
                    if (len(nums) == 1 and len(chars) == 2 and chars[1] in alphabet[:self.height] and int(nums[0]) in range(self.width)):
                        x = int(nums[0])
                        y = alphabet.index(chars[1])
                        self.field.flagTile(x,y)
                elif ((len(nums) == len(chars) == 1) and chars[0] in alphabet[:self.height] and int(nums[0]) in range(self.width)):
                    x = int(nums[0])
                    y = alphabet.index(chars[0])
                    if self.game_status == "first_move":
                        self.field.genBoard(x,y)
                    self.game_status = self.field.turnTile(x,y)
                else:
                    raise ValueError("Invalid or no input")
            except ValueError as e:
                self.view.setMsg("ValueError occured: " + str(e))
            except IndexError as e:
                self.view.setMsg("IndexError occured: " + str(e))
            except IOError as e:
                self.view.setMsg("IOError occured: " + str(e))

        if(self.game_status == "won"):
            self.view.setMsg("Game won, gratz!!")
        elif(self.game_status == "bombed"):
            self.view.setMsg(random.choice(["OOOhh you got served bro!",
                                            "You are LITTERALY the bomb! Well done!",
                                            "You blew up.. does that make you feel any better about yourself?",
                                            "You got your silly arse bombed"]))
        elif(self.game_status == "quitting"):
            self.view.setMsg("Quitting game.. you quitter!")
            if self.field.empty:
                self.field.genBoard(random.randint(0,self.width-1), random.randint(0,self.height-1))
        else:
            self.view.setMsg("unexpected game endning:", self.game_status)
        self.field.flipBoard()
        self.view.print(self.field.getBoard())
        self.view.getUserConfirm()


