#!/usr/bin/env python3

# The main module that brings everything together.

from sys import argv
import scripter
import sys
import time
import praw
import random
import requests
import os


reddit = praw.Reddit(
    client_id='BTwqpLqtP1t5qQ',
    client_secret='p0kQUlqO-1vyDZCy877B1M8nL4Q',
    user_agent='mac:iterm2-background:v0.0.1 (by /u/JavaOffScript)'
)


def print_usage():
    # Print the instructions of usage.
    print(
        '''
Usage:
    cliTerm2 [parameter]

Parameters:
    cliTerm2 [subreddit]   -   Grab a random image from 'subreddit', and make it your terminal background.
    cliTerm2 help          -   Display this help message.
''')


def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print('Downloading %s...' % (localFileName))
        with open(os.path.join('~/.cliTerm2/Images', localFileName), 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)


def change_terminal_background(arg):
    #next step here is to just check submission.url to see if it ends in jpg, then check if it's a common image upload site like imgur
    for submission in reddit.subreddit(arg).hot(limit=3):
        print(submission.url)
        if ('imgur.com' in submission.url):
            if ('imgur.com/a/' in submission.url):
                #it's an album, so skip
                continue
            elif ('jpg' in submission.url):
                #download image right away
                downloadImage(submission.url, 'downloadedPic.jpg')
                scripter.change_terminal()
                break
            else:
                #append .jpg to the end of the url then download image
                downloadImage(submission.url + '.jpg', 'downloadedPic.jpg')
                scripter.change_terminal()
                break
        else:
            print('not imgur')
        # print('imgur' in submission.url)
        # print('redd' in submission.url)


def single_argument_handler(arg):
    # Handle the logic for when there is only one command line parameter inputted.

    if arg == "help":
        print_usage()
    else:
        change_terminal_background(arg)


if __name__ == "__main__":
    # Entrance to the program.
    if len(argv) == 1:
        print("No command line arguments specified."
              "\nTry inputting in a subreddit with image posts."
              "\nOr type \"help\" to see all the commands.")
    elif len(argv) == 2:
        single_argument_handler(argv[1].lower())
    else:
        print("Only one command line argument is supported.")
