#!/usr/bin/env python3

# The main module that brings everything together.

from sys import argv
import scripter
import sys
import time
import praw
import requests
import os
import re


# this is a reddit key for an account I made specifically for this project. Please don't get this account banned, you will make me sad :(
reddit = praw.Reddit(
    client_id='BTwqpLqtP1t5qQ',
    client_secret='p0kQUlqO-1vyDZCy877B1M8nL4Q',
    user_agent='cliTerm2 (by /u/JavaOffScript)'
)


def printHelp():
    # Print the instructions of usage.
    print(
        '''
Usage:
    cliTerm2 [parameter1] [parameter2]

Parameters:
    cliTerm2 reddit [subreddit]   -   Grab a random image from 'subreddit', and make it your terminal background.
    cliTerm2 help                 -   Display this help message.
''')


def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print('Downloading %s...' % (localFileName))
        # testing
        with open(os.path.join('/Users/nick.gottschlich/Code/Personal/cliTerm2/./Images', localFileName), 'wb') as fo:
        # with open(os.path.join('~/.cliTerm2/Images', localFileName), 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)


def redditTerminalBackground(arg):
    for submission in reddit.subreddit(arg).random_rising(limit=25):

        # ensuring nobody gets fired
        if submission.over_18:
            print("THIS IS NSFW WE ARE SKIPPIN")
            continue

        print('trying to download: ' + submission.url)
        # the url ends in jpg, jpeg, or png, so we know we can download the image
        if (re.search('(.jpg|.jpeg|.png)$', submission.url)):
            # just force it to a jpg
            downloadImage(submission.url, 'downloadedPic.jpg')
            scripter.change_terminal()
            break
        #it didn't end in jpg, but it is on imgur
        elif ('imgur.com' in submission.url):
            if ('imgur.com/a/' in submission.url or 'imgur.com/gallery' in submission.url):
                #it's an album, so skip
                continue
            elif (re.search('(.gif|.gifv)$', submission.url)):
                #it's a gif, skip
                continue
            else:
                #append .jpg to the end of the url then download image
                downloadImage(submission.url + '.jpg', 'downloadedPic.jpg')
                scripter.change_terminal()
                break


def setTextColor(arg):
    


def argumentHandler(args):
    if args[1] == "help":
        printHelp()
    elif args[1] == 'reddit':
        redditTerminalBackground(args[2])
    elif args[1] == 'textcolor':
        setTextColor(args[2])
    else:
        print('Unrecognized argument, try "cliterm2 help"')


if __name__ == "__main__":
    # Entrance to the program.
    if len(argv) == 1:
        print("No command line arguments specified."
              "\nTry inputting in a subreddit with image posts."
              "\nOr type \"help\" to see all the commands.")
    else:
        argumentHandler(argv)
