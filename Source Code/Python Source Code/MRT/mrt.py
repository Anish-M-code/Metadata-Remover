""" 
A cross-platform open source file Metadata remover that
uses exiftool and ffmpeg to sanitize your files.
"""

import os
from shutil import copy, copy2

try:
    import MRT.commons as com
except ImportError:
    print("'commons' module was not found. Try reinstalling the module.")
    exit(1)


# Function to write given message to file named log in append mode.
def log_message(msg, file="log.txt"):
    with open(file, "a") as f:
        f.write(f"{msg}\n")
    return 


# Function to read and display metadata of a file.
def meta(file):
    os.system(f"{_EXIFTOOL} {file} > meta.txt")
    com.display("meta.txt")
    os.remove("meta.txt")
    return


# Copy and rename
def autoexif():
    if os.path.exists("exiftool(-k).exe") and not os.path.exists("exiftool.exe"):
        try:
            copy2("exiftool(-k).exe", "exiftool.exe")
        except Exception:
            # Fail silently.
            pass
    return 


def extract_metadata(file, mode='input'):
    if os.system(f"{_EXIFTOOL} {file} > {mode}.txt") != 0:
        com.error(f"An error has occurred while running {_EXIFTOOL} on {mode}.txt.")
        exit(1)


def img(image):
    # Exiftool renames the cleaned files automatically
    os.system(f"{_EXIFTOOL} -all= {image}")
    return


# Function to remove metadata from video file.
def vid(file):
    file_name = file.split('.')[:-1]
    file_extension = file.split('.')[-1]
    out_file = f"{file_name}_clean.{file_extension}"
    os.system(f"{_FFMPEG} -i {file} -map_metadata -1 -c:v copy -c:a copy {out_file}")

    com.cls()
    extract_metadata(out_file, 'output')
    copy("output.txt", "output_log.txt")
    return


IMAGE_EXTENSIONS = ("jpg", "gif", "bmp", "tiff", "jpeg", "png", "tif")
VIDEO_EXTENSIONS = ("mp4", "mov", "3gp", "ogv", "flv", "wmv", 
                    "avi", "mkv", "vob", "ogg", "webm")

def single_file(file_name: str):
    autoexif()

    if not os.path.exists(file_name):
        com.error(f"File {file_name} doesn't exist.")
        exit(1)

    # should include function detect to detect exiftool [imp]
    file_extension = file_name.split('.')[-1]
    if file_extension in IMAGE_EXTENSIONS:
        extract_metadata(file_name, 'input')
        copy("input.txt", "input_log.txt")
        img(file_name)
        extract_metadata(file_name,'output')
        copy("output.txt", "output_log.txt")

    elif file_extension in VIDEO_EXTENSIONS:
        extract_metadata(file_name, 'input')
        copy("input.txt", "input_log.txt")
        vid(file_name)

    else:
        com.error(f"Unsupported file format <{file_extension}>.\n")
        return -1


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
            log_message(f"{file_name}:No significant change!")

        os.remove("input.txt")
        os.remove("output.txt")

    else:
        print(f"{file_name}: No cleaning done!")
        log_message(f"{file_name}: No cleaning done!")

    return 


# Function to remove metadata of all images (filetype = i) or videos (filetype = v) from folder.
def bulk():
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
    return 


_START_DIR = os.getcwd()
_EXIFTOOL = os.path.join(_START_DIR, "exiftool.exe") if os.name == "nt" else "exiftool"
_FFMPEG = os.path.join(_START_DIR, "ffmpeg.exe") if os.name == "nt" else "ffmpeg"
