# flag=imp

try:
    from commons import *
    from mrt import *

except ImportError:
    print(" Critical Error :Required Modules were not Found!")
    x = input("\n Press any key to exit...")
    exit()

import os
from shutil import move, copy
import webbrowser as wb
from sys import exit
from time import sleep



try:
    import mutagen
except:
    x = os.system("py -m pip install mutagen")
    if x != 0:
        wb.open("https://pypi.org/project/mutagen/")
        print("Please install mutagen from https://pypi.org/project/mutagen/ ")
        sleep(5)
        exit(1)
    print("please close and restart this program!!!")
    sleep(5)
    exit(1)

# Function to display main menu()
def san():
    cls()
    print("\n ┣-━━━━━ Metadata Removal Tool ------|\n")
    print(" 1)Remove Metadata from a image.")
    print(" 2)Remove Metadata from a video.")
    print(" 3)Remove Metadata from a audio.")
    print(" 4)Remove Metadata from a Torrent.")
    print(" 5)Remove Metadata from all images in folder.")
    print(" 6)Remove Metadata from all videos in folder.")
    print(" 7)View Metadata in a file.")
    x = input("\n Enter command(1,2,3,4,5,6 or 7):")
    if x == "1":
        file = input("\n Enter image name:")
        singly(file, "i")
    elif x == "2":
        file = input("\n Enter Video name:")
        singly(file, "v")
    elif x == "3":
        file = input("\n Enter Audio File:")
        y = copy(file, "MRT")
        os.chdir("MRT")
        z = os.system("py mat2.py " + file)
        if z != 0:
            print("Something went wrong , metadata was not cleaned!!!")
            sleep(5)
        else:
            print("Metadata cleaned successfully !!!")
            y = move(file.split(".")[0] + ".cleaned." + file.split(".")[1], "..")
            os.remove(file)
            sleep(5)
        os.chdir("..")
    elif x == "4":
        file = input("\n Enter Torrent File:")
        y = copy(file, "MRT")
        os.chdir("MRT")
        z = os.system("py mat2.py " + file)
        if z != 0:
            print("Something went wrong , metadata was not cleaned!!!")
        else:
            print("Metadata cleaned successfully !!!")
            y = move(file.split(".")[0] + ".cleaned." + file.split(".")[1], "..")
            os.remove(file)
            sleep(5)
        os.chdir("..")
    elif x == "5":
        bulk("i")
    elif x == "6":
        bulk("v")
    elif x == "7":
        rb = input(" Enter Filename:")
        if os.path.exists(rb) == False:
            print("\n File Not Found!\n")
            wait()
            san()
            exit(0)
        meta(rb)
        wait()
    elif x.lower() == "c" or x.lower() == "close":
        exit()

# Perform checks to make sure ffmpeg and exiftool exist
ffmpeg()
exiftool()

# Get current working directory so we can return to it after san()
current = os.getcwd()

while True:

    san()
    # Reset working dir
    os.chdir(current)
