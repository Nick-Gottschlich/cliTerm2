# Used for creating, running and analyzing applescript and bash scripts.

import os

cwd = os.path.dirname(os.path.realpath(__file__))


def __terminal_script(anime):
    # Create the content for script that will change the terminal background image.
    content = "tell application \"iTerm\"\n"
    content += "\ttell current session of current window\n"
    content += "\t\tset background image to \"" + anime.get_path() + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def __wallpaper_script(anime):
    # Create the content for the script that will change the wallpaper.
    content = "tell application \"System Events\"\n"
    content += "\ttell current desktop\n"
    content += "\t\tset picture to \"" + anime.get_path() + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def __create_terminal_script(anime):
    # Create and save the script for changing the terminal background image.
    content = __terminal_script(anime)
    file = open(cwd + "/./Scripts/background.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __create_wallpaper_script(anime):
    # Create and save the script for changing the wallpaper.
    content = __wallpaper_script(anime)
    file = open(cwd + "/./Scripts/wallpaper.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __create_terminal_bash():
    # Create and save the run.sh that will execute the AppleScript if the correct run.sh doesn't already exist.
    content = "#!/bin/bash\n" + "osascript " + cwd + "/./Scripts/background.scpt"
    if open(cwd + "/./Scripts/run.sh", 'r').read() == content:
        return
    file = open(cwd + "/./Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __create_wallpaper_bash():
    # Create and save the run.sh that will execute the AppleScript if the correct run.sh doesn't already exist.
    content = "#!/bin/bash\n" + "osascript " + cwd + "/./Scripts/wallpaper.scpt"
    if open(cwd + "/./Scripts/run.sh", 'r').read() == content:
        return
    file = open(cwd + "/./Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()


def change_terminal(anime):
    # Create, save and run the bash script to change the terminal background.
    __create_terminal_script(anime)
    __create_terminal_bash()
    os.system(cwd + "/./Scripts/run.sh")


def change_wallpaper(anime):
    # Create, save and run the bash script to change the wallpaper.
    __create_wallpaper_script(anime)
    __create_wallpaper_bash()
    os.system(cwd + "/./Scripts/run.sh")


def determine_terminal_anime(db):
    # Print the current Anime that is being used as the terminal background.
    __determine_anime(db, "background.scpt")


def determine_wallpaper_anime(db):
    # Print the current Anime that is being used the wallpaper.
    __determine_anime(db, "wallpaper.scpt")


def __determine_anime(db, script_name):
    # Helper method to get the current Anime that is in the specified script.
    path = cwd + "/Scripts/" + script_name
    try:
        content = open(path, "r+").readlines()
    except FileNotFoundError:
        print("Missing File: ", path)
        return

    try:
        split = content[2].split('/')
        image_name = split[-1]  # The content after the final slash.
        image_name = image_name[:-6]  # Remove the .png and quotation at the end.
    except IndexError:
        print("Corrupt file:", path)
        return

    anime = db.get_anime(image_name)
    print(anime.get_id(), anime.get_name().capitalize())
