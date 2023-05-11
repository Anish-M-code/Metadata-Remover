# flag=imp

# Comment from 9x14S: variable assignment to input() statements only to require
# input before an action are irrelevant. 

# This is the "root" module, it doesn't import any other from the package, so start from
# here if you want to modify it heavily

# This is the common library developed to satisfy the needs of commandline python applications .
# It contains necessary std libraries and basic functions for its users.

'''Functions used: 
fileRemove
packageDetect
taskStart/End/Fail
wait
printFile
copyFile
checkDependencies
cls
'''
try:
    # Are ALL these modules actually used?
    import hashlib, time, os, platform, webbrowser, getpass, shutil

except ImportError:
    # Deleted redundant second print function and unaccessed variable (x) to input function, 
    # for which it is not needed
    print("Critical Error: Necessary Python Modules are missing! \nCommons module couldnot satisfy all the dependencies!")
    input("Press any key to exit...")
    exit()

# Deletes file after checking if it exists or not.
def fileRemove(file):
    if os.path.exists(file):
        os.remove(file)

# Function to open website if prerequisite software is not found,
def packageDetect(cmd, webSite, shortName, package):
    if OS: # checks if os is windows
        if os.system(cmd + ">chk") != 0:
            os.system("cls")
            print(cmd)
            print(f"\nError: {package} is not detected!")
            print(f"\nA webpage to {shortName} is being opened. ")
            webbrowser.open(webSite)
            wait()
            fileRemove("chk")
            exit()
    else:
        if os.system(cmd + ">chk") != 0:
            os.system("clear")
            print(f"\nError: {package} is not detected!")
            wait()
            fileRemove("chk")
            exit()

# These four functions could be replaced for something better maybe
def taskStart():
    print("\n<-----Task Started----->\n")
def taskEnd():
    print("\n<-----Task Completed----->\n")
def taskFail():
    print("\n<-----Task Failed !----->\n")
def wait():
    input("\nPress any key to continue...\n")

# Function to Display contents of text file.
def printFile(file):
    with open(file, "r") as f:
        # This should be replaced with the like of a do-while loop
        s = f.read(1024)
        print(s)
        while len(s) > 0:
            s = f.read(1024)
            print(s)

def checkDependencies():
    packageDetect("gpg --version", "https://gpg4win.org", "gpg4win", "Gnupg")
    packageDetect("exiftool -h", "https://exiftool.org", "exiftool", "Exiftool")
    packageDetect("ffmpeg --help", "https://ffmpeg.org/", "ffmpeg", "ffmpeg")

# Function to copy textfile.
def copyFile(fileIn, fileOut):
    if os.path.exists(fileIn):
        shutil.copy(fileIn, fileOut)
        
# Clear the screen depending on the OS
def cls():
    if OS:
        os.system("cls")
    else:
        os.system("clear")

# To save time, do the computation once and then use boolean values
if os.name == "nt":
    OS = True
else:
    OS = False