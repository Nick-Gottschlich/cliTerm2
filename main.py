#!/usr/bin/env python3

# The main module that brings everything together.

from sys import argv
from database import Database
import scripter
import sys
import time


def print_list(list_of_items):
    # Print all the items in a list. Used for printing each Anime from a particular region.
    for item in list_of_items:
        print(item)


def print_columns(items):
    # Print a list as multiple columns instead of just one.
    rows = []
    items_per_column = int(len(items) / 4) + 1

    for index in range(0, len(items)):
        anime = items[index]

        if not anime.is_extra():
            name = anime.get_id() + " " + str(anime.get_name()).capitalize()
        else:
            name = "--- " + anime.get_name()

        name = name.ljust(20)

        if len(rows) < items_per_column:
            rows.append(name)
        else:
            rows[index % items_per_column] += name

    print_list(rows)


def prefix_search(db, arg):
    # Find all Anime in database, db, with the prefix, arg.
    result = db.names_with_prefix(arg)
    if len(result) == 0:
        print("No Anime found with prefix '" + arg + "'.")
    else:
        print_columns(result)


def print_extra(db):
    # Print all the 'Extra' Anime from the 'Extra' folder.
    result = db.get_extra()
    if len(result) == 0:
        print("No Anime were found in Images/Extra.")
    else:
        print_columns(result)


def print_usage():
    # Print the instructions of usage.
    print(
        '''
Usage:
    anime [parameter]

Parameters:
    [name]        -   Change the terminal background to the specified Anime.
    [index]       -   Change the terminal background to a Anime by its index.
    [region]      -   List all the Anime of the specified region.
    [one letter]  -   List all Anime who's names begin with a particular letter.
    [two letters] -   List all Anime who's names begin with those two letters.

Other Parameters:
    anime all             -   List all the Anime supported.
    anime extra           -   List all the Anime from the 'Extra' folder.
    anime random          -   Change the terminal background to a random Anime.
    anime ?               -   Identify the current Anime in the terminal.
    anime _pikachu        -   Change the wallpaper to the specified Anime.
    anime _random         -   Change the wallpaper to a random Anime.
    anime _?              -   Identify the current Anime in the wallpaper.
    anime slideshow       -   Iterate through each Anime.
    anime help            -   Display this menu.
''')


def slideshow(db, start, end):
    # Show each Anime in order, one by one.
    try:
        for x in range(start, end):
            anime = db.get_anime(x)
            scripter.change_terminal(anime)
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("Program was terminated.")
        sys.exit()


def change_terminal_background(db, arg):
    # Change the terminal background to the specified Anime, if it exists.
    if arg in db:
        anime = db.get_anime(arg)
        scripter.change_terminal(anime)
    else:  # If not found in the database, try to give suggestions.
        suggestions = db.names_with_infix(arg)
        if len(suggestions) == 0:
            print("No such Anime was found and no suggestions are available.")
        elif len(suggestions) == 1:
            scripter.change_terminal(suggestions[0])
            print("Did you mean " + suggestions[0].get_name().capitalize() + "?")
            scripter.change_terminal(suggestions[0])
        else:
            print("Did you mean " + suggestions[0].get_name().capitalize() + "?")
            print("Other suggestions:")
            print_columns(suggestions[1:])
            scripter.change_terminal(suggestions[0])


def change_wallpaper(db, arg):
    # Change the wallpaper to the specified Anime, if it exists.
    if arg in db:
        anime = db.get_anime(arg)
        scripter.change_wallpaper(anime)
    else:  # If not found in the database, try to give suggestions.
        suggestions = db.names_with_infix(arg)
        if len(suggestions) == 0:
            print("No such Anime was found and no suggestions are available.")
        elif len(suggestions) == 1:
            scripter.change_wallpaper(suggestions[0])
            print("Did you mean " + suggestions[0].get_name().capitalize() + "?")
            scripter.change_wallpaper(suggestions[0])
        else:
            print("Result: " + arg)
            print("Did you mean " + suggestions[0].get_name().capitalize() + "?")
            print("Other suggestions:")
            print_columns(suggestions[1:])
            scripter.change_wallpaper(suggestions[0])


def single_argument_handler(arg):
    # Handle the logic for when there is only one command line parameter inputted.
    db = Database()

    # If there is an escape code, then change the wallpaper, not the terminal.
    if str(arg).startswith("_"):
        escape_code = True
        arg = arg[1:]
    else:
        escape_code = False

    if len(arg) < 3 and arg.isalpha():
        prefix_search(db, arg)
    elif arg == "extra":
        print_extra(db)
    elif arg == "help":
        print_usage()
    elif arg == "random" and escape_code:
        change_wallpaper(db, db.get_random().get_name())
    elif arg == "random":
        change_terminal_background(db, db.get_random().get_name())
    elif arg == "slideshow":
        slideshow(db, 1, 494)
    elif arg == "?" and escape_code:
        scripter.determine_wallpaper_anime(db)
    elif arg == "?":
        scripter.determine_terminal_anime(db)
    elif escape_code:
        change_wallpaper(db, arg)
    else:
        change_terminal_background(db, arg)


if __name__ == "__main__":
    # Entrance to the program.
    if len(argv) == 1:
        print("No command line arguments specified."
              "\nTry typing in a Anime name or number."
              "\nOr type \"help\" to see all the commands.")
    elif len(argv) == 2:
        single_argument_handler(argv[1].lower())
    else:
        print("Only one command line argument is supported.")
