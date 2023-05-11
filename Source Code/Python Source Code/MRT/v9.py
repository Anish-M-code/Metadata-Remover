# flag=imp

'''Functions used:
singly (from )
bulk (from )
meta (from )
success
mainV9
checkDependencies (from commons)
wait (from commons)
cls (from commons)

'''

from sys import exit
from time import sleep
from shutil import move, copy

import webbrowser as wb
import os

try:
    from commons import *
    from mrt import *
    
except ImportError:
    print("Critical Error: required modules were not Found!")
    wait()
    exit()

try:
    # What's the point of mutagen if it isn't accessed?
    import mutagen
except:
    if input("The module mutagen has not been found, want to install it [y/n]?: ").lower() == "y":
        os.system("py -m pip install mutagen")
    else:
        print("Please install mutagen from https://pypi.org/project/mutagen/ and then run this program again. ")
        sleep(5)
        exit(1)
    print("This program will now close, restart once it installs for the changes to have effect. ")
    sleep(5)
    exit(1)

def success(file):
    print("The metadata was cleaned successfully. ")
    splitFile = file.split(".")
    move(splitFile[0] + ".cleaned." + splitFile[1], "..")
    os.remove(file)
    sleep(5)
    
# Main function of the program
def mainV9():
    cls()
    print("\n |------ Metadata Removal Tool ------|\n")
    print(" 1)Remove Metadata from an image file.")
    print(" 2)Remove Metadata from a video file.")
    print(" 3)Remove Metadata from an audio file.")
    print(" 4)Remove Metadata from a Torrent file.")
    print(" 5)Remove Metadata from all images in a folder.")
    print(" 6)Remove Metadata from all videos in a folder.")
    print(" 7)View Metadata in a file.")
    menuSelection = input("\nEnter selection number:")
    # I preferred to use the match function instead of chaining if-elif statements
    # as I believe it looks better and functionally it is the same.
    match menuSelection:
        case "1":
            file = input("\n Enter image name:")
            singly(file, "i")
        case "2":
            file = input("\n Enter Video name:")
            singly(file, "v")
        case "3":
            file = input("\n Enter Audio File:")
            copy(file, f".{os.path.sep}MRT")
            os.chdir("MRT")
            if not os.system("py mat2.py " + file):
                print("Something went wrong. Possibly the metadata was not cleaned. Please try again. ")
                sleep(5)
            else:
                success(file)
            os.chdir("..")
        case "4":
            file = input("\n Enter Torrent File:")
            copy(file, "MRT")
            os.chdir("MRT")
            if not os.system("py mat2.py " + file):
                print("Something went wrong, the metadata was not removed.")
            else:
                success(file)
            os.chdir("..")
        case "5":
            bulk("i")
        case "6":
            bulk("v")
        case "7":
            file = input("Enter file name or path: ")
            if not os.path.exists(file):
                print("\n File Not Found!\n")
                wait()
                exit(0)
            metaView(file)
            wait() 
# Perform checks to make sure ffmpeg, gpg and exiftool exist
checkDependencies()

# The main function only needs to be run once, and the current working directory resets automatically
# after the program ends, so no reason for it to be changed back.
mainV9()