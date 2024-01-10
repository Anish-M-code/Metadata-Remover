""" 
This is the common library developed to satisfy the needs of the main program.
It contains the necessary standard libraries and other basic functions.
"""

# Standard library modules, guaranteed to be available
import platform
import os
import sys

def wait():
    """Pause execution."""
    input("\nPress any key to continue...")


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

        If you feel it negatively impacts on the readability and adds nothing 
        of value, hit me up on github
        and we'll discuss this."""
    global _PLAT
    global _CLS_PLAT
    global _GPG_SITE
    global _GPG_CMD
    _PLAT = platform.platform().lower()

    if "windows" in _PLAT:
        _CLS_PLAT = "cls"
        _GPG_SITE = "https://gpg4win.org"
        _GPG_CMD = "gpg4win"

    elif "linux" in _PLAT or "darwin" in _PLAT:
        _CLS_PLAT = "clear"
        _GPG_SITE = "PLACEHOLDER FOR POSIX-LIKE SYSTEMS"
        _GPG_CMD = "gpg"

    else:
        _CLS_PLAT = "false"
        _GPG_SITE = "PLACEHOLDER FOR OTHER PLATFORMS"
        _GPG_CMD = "PLACEHOLDER FOR OTHER PLATFORMS"
        error("Unsupported platform. Internal system checking disabled.\n")


#+----------------File I/O functions----------------+


def rmfile(file):
    """Checks if a file exists, if so, removes it."""
    if os.path.exists(file):
        os.remove(file)


def display(file):
    """Opens and reads from a file, then prints."""
    with open(file, "r", encoding="utf-8") as display_file:
        print(display_file.read(), end='')


#+----------------Text display functions----------------+


def error(errstr: str) -> None:
    """Wrapper to print to stderr. Might be replaced with the
    logging module."""
    sys.stderr.write(errstr)


def cls():
    """Sends a platform-appropriate clear screen command."""
    os.system(_CLS_PLAT)


def get_website(cmd, web, snam, pkg):
    """Prints the missing package's website so the user can 
    download the tool."""
    if os.system(cmd + "> chk.mtd") != 0:
        cls()
        error(
                f"\nError: Package {snam}/{pkg} wasn't found!\n"
                f"Please head to {web} to get instructions on how to"
                "install the package before continuing.\n"
             )
        wait()
        sys.exit(1)
    rmfile("chk.mtd")


# Unused
# def gpg():
#    print("Checking GPG...")
#    get_website("gpg --version", _GPG_SITE, _GPG_CMD, "Gnupg")
#    print("GPG found!")


def exiftool():
    """Check if Exiftool exists."""
    print("Checking Exiftool...")
    get_website("exiftool -h", "https://exiftool.org", "exiftool", "Exiftool")
    print("Exiftool found!")


def ffmpeg():
    """Check if ffmpeg exists."""
    print("Checking ffmpeg...")
    get_website("ffmpeg --help", "https://ffmpeg.org/", "ffmpeg", "ffmpeg")
    print("ffmpeg found!")


def start():
    """Prints start of task delimeter."""
    print("\n┣━━━━━ Task Started ━━━━━┫\n")


def end():
    """Prints end of task delimeter."""
    print("\n┣━━━━━ Task Completed ━━━━━┫\n")


def tskf():
    """Prints failed task delimeter."""
    print("\n┣━━━━━ Task Failed! ━━━━━┫\n")


setup()
