""" 
This is the common library developed to satisfy the needs of the main program.
It contains the necessary standard libraries and other basic functions.
"""

def wait():
    _WAIT_FUNC()


# Standard library modules, guaranteed to be available
import platform
import os
import sys
from shutil import copy2


# Global constants
# Not used yet
_EXIFTOOL = "https://exiftool.org"
_FFMPEG = "https://ffmpeg.org/"

# Must be set up before using 
_PLAT: str
_CLS_PLAT: str
_GPG_SITE: str
_GPG_CMD: str


# Sets up the global constants about the platform
def setup():
    """
    Sets up a bunch on constants depending on the platform. This is supposed to make the 
        program have less 'if os.name == whatever' statements and also to concentrate all
        hard-to-read elements into a single place. 

        If you feel it negatively impacts on the readability and adds nothing of value, hit me up on github
        and we'll discuss this.
    """
    global _PLAT 
    global _CLS_PLAT
    global _GPG_SITE
    global _GPG_CMD
    global _WAIT_FUNC
    _PLAT = platform.platform()

    if _PLAT == "Windows":
        _CLS_PLAT = "cls"
        _GPG_SITE = "https://gpg4win.org" 
        _GPG_CMD = "gpg4win"
        def _WAIT_FUNC():
            input("\nPress any key to exit...")

    elif _PLAT in ["Linux", "Darwin"]:
        _CLS_PLAT = "clear"
        _GPG_SITE = "PLACEHOLDER FOR POSIX-LIKE SYSTEMS"
        _GPG_CMD = "gpg"
        # In POSIX-like systems, a pause function wouldn't be needed
        def _WAIT_FUNC():
            pass

    else:
        _CLS_PLAT = "false"
        _GPG_SITE = "PLACEHOLDER FOR OTHER PLATFORMS"
        _GPG_CMD = "PLACEHOLDER FOR OTHER PLATFORMS"
        error("Unsupported platform. Internal system checking disabled.\n")


"""+----------------File I/O functions----------------+"""


# Deletes file after checking if it exists or not.
def rmfile(f):
    if os.path.exists(f):
        os.remove(f)


# Function to copy textfile.
def copy(file1, file2):
    #TODO: Check that the output files are formatted correctly
    copy2(file1, file2, follow_symlinks=False)


# Function to Display contents of text file.
def display(file):
    with open(file, "r") as f:
        for data in f.read(1024):
            print(data)



"""+----------------Text display functions----------------+"""

# Print errors to stderr
def error(errstr: str) -> None:
    sys.stderr.write(errstr)


# Clearscreen
def cls():
    os.system(_CLS_PLAT)


# Function to open website if prerequisite software is not found in PC.
def get_website(cmd, web, snam, pkg):
    if os.system(cmd + "> chk.mtd") != 0:
        cls()
        error(
                f"\nError: Package {snam}/{pkg} wasn't found!\n"
                f"Please head to {web} to get instructions on how to"
                "install the package before continuing.\n"
             )
        wait()
        exit(1)
    rmfile("chk.mtd")


def gpg():
    get_website("gpg --version", _GPG_SITE, _GPG_CMD, "Gnupg")


def exiftool():
    get_website("exiftool -h", "https://exiftool.org", "exiftool", "Exiftool")


def ffmpeg():
    get_website("ffmpeg --help", "https://ffmpeg.org/", "ffmpeg", "ffmpeg")


def start():
    print("\n┣━━━━━ Task Started ━━━━━┫\n")


def end():
    print("\n┣━━━━━ Task Completed ━━━━━┫\n")


def tskf():
    print("\n┣━━━━━ Task Failed! ━━━━━┫\n")




setup()
