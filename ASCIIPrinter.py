import os
import platform

logo = """\
,------.,--.   ,--.,---. ,--.   ,--.,------.,------.,------. ,------.,------.  
|  .--. '\  `.'  /'   .-'|  |   |  ||  .---'|  .---'|  .--. '|  .---'|  .--. ' 
|  '--' | '.    / `.  `-.|  |.'.|  ||  `--, |  `--, |  '--' ||  `--, |  '--'.' 
|  | --'    |  |  .-'    |   ,'.   ||  `---.|  `---.|  | --' |  `---.|  |\  \  
`--'        `--'  `-----''--'   '--'`------'`------'`--'     `------'`--' '--'
"""
logo_subtext = "\t -The Game"

msg_container="""\
  /-------------------------------------------------------------------------/
 /                                                                         /
/-------------------------------------------------------------------------/"""

class ASCIIPrinter(object):
    """class for printing the pysweeper board to the terminal"""

    def __init__(self):
        self.msg = msg_container
        self.body = ""
        self.default_prompt="-> "
        self.default_confirm="Press Enter.. "
        if platform.system() == 'Windows':
            self.clear_cmd = 'CLS'
        elif platform.system() == 'Linux':
            self.clear_cmd = 'clear'

    def flush(self):
        """Print current inputted board to stdout"""
        os.system(self.clear_cmd)
        print(logo)
        print(logo_subtext,'\n')
        print(self.msg,'\n')
        print(self.body)
        self.body = ""

    def setMsg(self, text):
        """Add a text to the msg field"""
        msg_split = self.msg.splitlines()
        msg_split[1] = " /   " + text + " "*(70-len(text)) + "/"
        self.msg = '\n'.join(msg_split)

    def pushToBody(self, text):
        """Add content to the body field"""
        self.body += (text + "\n")

    def print(self, text):
        """Add content to the body field and flush"""
        self.body = (text + "\n")
        self.flush()

    def reset(self):
        """Reset view default"""
        self.msg = msg_container
        self.body = ""

    def getUserInput(self):
        """Wait for user input"""
        inp = input(self.default_prompt)
        return inp

    def getUserConfirm(self):
        """Wait for user confirmation"""
        input(self.default_confirm)

# p = ASCIIPrinter()

# p.setMsg("this is the new shit")

# p.flush()
