import termcolor

colors = ["grey","red","green","yellow","blue","magenta","cyan","white"]

def colorize(text, fgcolor, bgcolor):
    if (set([bgcolor,fgcolor]) <= set(colors)):
        return termcolor.colored(text,fgcolor,("on_"+bgcolor))
    else:
        raise ValueError("Unknown color input",fgcolor,bgcolor)

def colorByContent(slot):
    colored_slot = ""
    if slot == " ":
        colored_slot = colorize(" "+slot+" ", "white", "grey")
    elif slot == "-":
        colored_slot = colorize(" "+slot+" ", "grey", "white")
    elif slot == "X":
        colored_slot = colorize(" "+slot+" ", "grey", "red")
    elif slot == "*":
        colored_slot = colorize(" "+slot+" ", "red", "white")
    elif slot == "F":
        colored_slot = colorize(" "+slot+" ", "green", "white")
    elif slot == "U":
        colored_slot = colorize(" "+slot+" ", "red", "white")
    elif slot == "1":
        colored_slot = colorize(" "+slot+" ", "white", "blue")
    elif slot == "2":
        colored_slot = colorize(" "+slot+" ", "white", "green")
    elif slot == "3":
        colored_slot = colorize(" "+slot+" ", "white", "red")
    elif slot == "4":
        colored_slot = colorize(" "+slot+" ", "white", "yellow")
    elif slot == "5":
        colored_slot = colorize(" "+slot+" ", "white", "magenta")
    return colored_slot
