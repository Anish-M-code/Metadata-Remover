"""Main file to be run."""

import sys
import os
from shutil import move, copy


try:
    import commons as com
except ImportError:
    print("Required module <commons.py> was not found.")
    print("Try reinstalling the module and try again.")
    input("\nPress any key to exit...")
    sys.exit(1)


try:
    import mrt
except ImportError:
    print("Required module <mrt.py> was not found.")
    print("Try reinstalling the module and try again.")
    input("\nPress any key to exit...")
    sys.exit(1)



# Tries to check if the module mutagen exists, even if not used in this file
try:
    import mutagen
    del mutagen
except ImportError:
    com.error(
            "Module <mutagen> was not found. Please install it by running "
            "'python3 -m pip install mutagen' and then rerun this program.")
    com.wait()
    sys.exit(1)


def menu():
    """Displays the menu and handles choices."""
    while True:
        os.chdir(START_DIR)
        com.cls()
        print("┣━━━━━ MRT module stable release version 0.2.4 ━━━━━┫")
        print(" ╔═══════════════════════════════════╗ ")
        print(" ║       Metadata Removal Tool       ║ ")
        print(" ╚═══════════════════════════════════╝ ")
        print("")
        print(" 1 ▸ Remove Metadata from a single image.")
        print(" 2 ▸ Remove Metadata from a single video.")
        print(" 3 ▸ Remove Metadata from an audio file.")
        print(" 4 ▸ Remove Metadata from a Torrent file.")
        print(" 5 ▸ Remove Metadata from all images in a folder.")
        print(" 6 ▸ Remove Metadata from all videos in a folder.")
        print(" 7 ▸ View Metadata in a file.")
        print(" Any other key exits.")
        print("")

        choice = input("Enter choice (1, 2, 3, 4, 5, 6 or 7): ")
        print("")
        match choice:
            case '1':
                file = input("Image filepath: ")
                mrt.single_file(file)

            case '2':
                file = input("Video filepath: ")
                mrt.single_file(file)

            case '3' | '4' as t_or_f:
                if t_or_f == '3':
                    file = input("Audio file: ")
                else:
                    file = input("Torrent file: ")

                copy(file, "MRT")
                os.chdir("MRT")
                result = os.system(f"python3 mat2.py {file}")
                if result != 0:
                    com.error(
                            "Something went wrong, the metadata probably wasn't cleaned.\n"
                            "Aborting."
                              )
                    sys.exit(1)
                else:
                    # Get only the name, not the extension
                    file_name = '.'.join(file.split('.')[:-1])
                    # Get extension
                    file_extension = file.split('.')[-1]
                    # Make new, great name
                    new_name = f"{file_name}_cleaned_.{file_extension}"
                    move(new_name, "..")
                    print("Metadata cleaned successfully.")

            case '5':
                mrt.bulk()

            case '6':
                mrt.bulk()

            case '7':
                read_md = input("Filepath: ")
                if not os.path.exists(read_md):
                    com.error(f"File '{read_md}' doesn't exist.")
                    com.wait()
                    sys.exit(1)
                mrt.meta(read_md)

            case _:
                print("Bye!")
                sys.exit(0)



# Get current working directory so we can return to it after each loop
START_DIR = os.getcwd()
def main():
    """Run required checks and set up the program."""
    # Perform checks to make sure ffmpeg and exiftool exist
    com.ffmpeg()
    com.exiftool()

    # Make directory and run
    os.makedirs("MRT", exist_ok=True)
    menu()

if __name__ == "__main__":
    main()
