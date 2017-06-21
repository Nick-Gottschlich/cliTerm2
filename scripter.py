# Used for creating, running and analyzing applescript and bash scripts.

import os

testPath = '/Users/nick.gottschlich/Code/Personal/cliTerm2/'

def __terminal_script():
    # Create the content for script that will change the terminal background image.
    content = "tell application \"iTerm\"\n"
    content += "\ttell current session of current window\n"
    content += "\t\tset background image to \"/Users/nick.gottschlich/Code/Personal/cliTerm2/./Images/downloadedPic.jpg\"\n"
    # content += "\t\tset background image to ~/.cliTerm2/Images/downloadedPic.jpg\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def __create_terminal_script():
    # Create and save the script for changing the terminal background image.
    content = __terminal_script()
    file = open(testPath + "/./Scripts/background.scpt", "wb")
    # file = open("~/.cliTerm2/Scripts/background.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __create_terminal_bash():
    # Create and save the run.sh that will execute the AppleScript if the correct run.sh doesn't already exist.
    content = "#!/bin/bash\n" + "osascript " + testPath + "/./Scripts/background.scpt"
    # content = "#!/bin/bash\n" + "osascript " + "~/.cliTerm2/./Scripts/background.scpt"
    if open(testPath + "/./Scripts/run.sh", 'r').read() == content:
    # if open("~/.cliTerm2/Scripts/run.sh", 'r').read() == content:
        return
    file = open(testPath + "/./Scripts/run.sh", 'wb')
    # file = open("~/.cliTerm2/./Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()


def change_terminal():
    # Create, save and run the bash script to change the terminal background.
    __create_terminal_script()
    __create_terminal_bash()
    os.system(testPath + "/./Scripts/run.sh")
    # os.system("~/.cliTerm2/./Scripts/run.sh")
