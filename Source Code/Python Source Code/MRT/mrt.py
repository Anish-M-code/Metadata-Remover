""" 
A cross-platform open source file Metadata remover that
uses exiftool and ffmpeg to sanitize your files.
"""

import os
import sys
from shutil import SameFileError, copy, copy2

try:
    import commons as com
except ImportError:
    print("'commons' module was not found. Try reinstalling the module.")
    sys.exit(1)


def log_message(msg, file="log.txt"):
    """Log the action in the log file."""
    if os.path.getsize(file) > 1024 * 1024: # 1 MB
        os.remove(file)
    with open(file, "a", encoding="utf-8") as log_file:
        log_file.write(f"{msg}\n")


def meta(file):
    """Read metadata from file."""
    os.system(f"{_EXIFTOOL} {file} > meta.txt")
    com.display("meta.txt")
    com.wait()
    com.cls()
    os.remove("meta.txt")


def autoexif():
    """Checks for a misnamed exiftool."""
    if os.path.exists("exiftool(-k).exe") and not os.path.exists("exiftool.exe"):
        try:
            copy2("exiftool(-k).exe", "exiftool.exe")
        except (SameFileError, OSError):
            # Fail silently.
            pass


def extract_metadata(file, mode='input'):
    """Extracts metadata from the file and writes to file depending on 
       mode."""
    if os.system(f"{_EXIFTOOL} {file} > {mode}.txt") != 0:
        com.error(f"An error has occurred while running {_EXIFTOOL} on {mode}.txt.")
        sys.exit(1)


def img(image):
    """Handle image files. Gives prompt to remove originals."""
    while True:
        choice = input("Remove original copies? (y/N): ").lower().strip()
        if choice in ['y', 'n']:
            break

    # Exiftool renames the cleaned files automatically
    os.system(f"{_EXIFTOOL} -all= {image}")
    if choice == 'y':
        os.remove(f"{image}_original")


def vid(file):
    """Handle video files."""
    file_name = file.split('.')[:-1]
    file_extension = file.split('.')[-1]
    out_file = f"{file_name}_clean.{file_extension}"
    os.system(f"{_FFMPEG} -i {file} -map_metadata -1 -c:v copy -c:a copy {out_file}")

    com.cls()
    extract_metadata(out_file, 'output')
    copy("output.txt", "output_log.txt")


IMAGE_EXTENSIONS = ("jpg", "gif", "bmp", "tiff", "jpeg", "png", "tif")
VIDEO_EXTENSIONS = ("mp4", "mov", "3gp", "ogv", "flv", "wmv",
                    "avi", "mkv", "vob", "ogg", "webm")

def single_file(file_name: str):
    """Determine filetype and call appropriate function."""
    if not os.path.exists(file_name):
        com.error(f"File {file_name} doesn't exist.")
        sys.exit(1)

    file_extension = file_name.split('.')[-1]
    if file_extension in IMAGE_EXTENSIONS:
        extract_metadata(file_name, 'input')
        img(file_name)
        extract_metadata(file_name,'output')

    elif file_extension in VIDEO_EXTENSIONS:
        extract_metadata(file_name, 'input')
        vid(file_name)

    else:
        com.error(f"Unsupported file format <{file_extension}>.\n")

    if os.path.exists("input.txt") and os.path.exists("output.txt"):
        in_size = os.path.getsize("input.txt")
        out_size = os.path.getsize("output.txt")

        if out_size == 0:
            com.error("An error has occured while processing file.\n"
                      "Size of file output.txt cannot be zero.")

        elif in_size > out_size:
            print(f"{file_name}: Metadata removed successfully!")
            log_message("{file_name}: Metadata removed successfully!")

        elif in_size == out_size:
            print(f"{file_name}: No significant change!")
            log_message(f"{file_name}: No significant change!")

        os.remove("input.txt")
        os.remove("output.txt")

    else:
        print(f"{file_name}: No cleaning done!")
        log_message(f"{file_name}: No cleaning done!")


# TODO: Add checks for each file
def bulk():
    """Handle multiple files by checking the if all files 
    are of the same type."""
    com.start()
    loc = input("Enter folder: ")
    os.chdir(loc)
    for file in os.listdir():
        single_file(file)

    print("\nOutput\n")
    log_file = "log.txt"
    if os.path.exists(log_file):
        com.display(log_file)
        os.remove(log_file)

    print("Done!")
    com.end()
    com.wait()


_START_DIR = os.getcwd()
_EXIFTOOL = os.path.join(_START_DIR, "exiftool.exe") if os.name == "nt" else "exiftool"
_FFMPEG = os.path.join(_START_DIR, "ffmpeg.exe") if os.name == "nt" else "ffmpeg"
