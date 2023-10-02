# flag=imp

""" 
An Cross-platform opensource Metadata Remover using exiftool and ffmpeg to sanitize your images before posting on internet.
"""

try:

    from commons import *


except ImportError:
    print(" The commons Modules Not Found! in mrt")
    x = input()
    exit()

# Runs correct clear command for OS
def clear():
  if os.name == "nt": # Windows
    os.system("cls")
  else:
    os.system("clear")

# Function to write given message to file named log in append mode.
def w(msg, file="log"):
    with open(file, "a+") as f:
        f.write("\n" + msg)


# Function to read and display metadata of a file.
def meta(file):
    if (os.name == "nt"):
      os.system(os.path.join(cwd,"exiftool ") + file + " >meta.txt")
    else:
      os.system("exiftool " + file + " >meta.txt")
    display("meta.txt")
    os.remove("meta.txt")


# Function to rename exiftool(-k).exe as exiftool.exe in windows.
def autoexif():
    if os.path.exists("exiftool(-k).exe"):
        try:
            os.rename("exiftool(-k).exe", "exiftool.exe")
        except FileExistsError:
            print("Exiftool Already Exists!...\n")
            os.remove("exiftool(-k).exe")

# Get the current working directory that the executables are in
cwd = os.getcwd()

# Write either input log (i) or output log (o) using correct executable filepath.
# This deprecates old bcopy() function which copied the binary into the working directory for windows
def writeToInputOutput(x,mode='i'):
  if mode == 'i':
    if (os.name == "nt"):
      os.system(os.path.join(cwd,"exiftool ") + x + ">input.txt")
    else:
      os.system("exiftool " + x + ">input.txt")
  if mode == 'o':
    if (os.name == "nt"):
      os.system(os.path.join(cwd,"exiftool ") + x + ">output.txt")
    else:
      os.system("exiftool " + x + ">output.txt")


# Function to remove metadata from image file.
def img(x):

    if x.lower().endswith(".tiff") or x.lower().endswith(".tif"):
        if (os.name == "nt"):
          os.system(os.path.join(cwd,"exiftool -all=  ") + x)
          return
        else:
          os.system("exiftool -all=  " + x)
          return
    if (os.name == "nt"):
      os.system(os.path.join(cwd,"exiftool ") + x + " -all=")
    else:
      os.system("exiftool " + x + " -all=")


# Function to remove metadata from video file.
def vid(x):
    # ffmpeg()
    count = -1
    for i in x:
        count += 1
        if x[count] == ".":
            break
    file = x[:count]
    ext = x[count:]
    y = file + "_clean" + ext
    if (os.name == "nt"):
      os.system(os.path.join(cwd,"ffmpeg -i ") + x + " -map_metadata -1 -c:v copy -c:a copy " + y)
    else:
      os.system("ffmpeg -i " + x + " -map_metadata -1 -c:v copy -c:a copy " + y)
    clear()
    writeToInputOutput(y,'o')
    copy("output.txt", "output_log.txt")


# Function to remove metadata from single image or video file. It uses img() and vid() internally.
# x denotes file given as input , y can be either i for images or v for videos , mode can be n for normal mode, or b for bulk processing mode.
def singly(x, y, mode="n"):
    autoexif()
    flag = 0

    if os.path.exists(x) == False:
        print("File Doesn't Exist!\n")
        time.sleep(3)
        exit(0)

    # should include function detect to detect exiftool [imp]
    if y.lower() == "i":
        v = (".jpg", ".gif", ".bmp", ".tiff", ".jpeg", ".png", ".tif")
        for i in v:
            if x.lower().endswith(i):
                writeToInputOutput(x,'i')
                copy("input.txt", "input_log.txt")
                img(x)
                flag = 1
                writeToInputOutput(x,'o')
                copy("output.txt", "output_log.txt")

    elif y.lower() == "v":
        # ffmpeg()
        v = (
            ".mp4",
            ".mov",
            ".webm",
            ".ogv",
            ".flv",
            ".wmv",
            ".avi",
            ".mkv",
            ".vob",
            ".ogg",
            ".3gp",
        )
        for i in v:
            if x.lower().endswith(i):
                writeToInputOutput(x,'i')
                copy("input.txt", "input_log.txt")
                vid(x)
                flag = 1

    else:
        print(" Unsupported File Format!")
        return 0

    if mode == "n":

        if flag == 0:
            print("\n Invalid File for processing!")
            wait()
            exit()

    if (os.path.exists("input.txt") == True) and (os.path.exists("output.txt") == True):
        if os.path.getsize("output.txt") == 0:
          clear()
          print(" Error Processing File!")
        elif os.path.getsize("input.txt") > os.path.getsize("output.txt"):
            print(x + ": Metadata removed successfully!")
            w(x + ": Metadata removed successfully!")
        elif os.path.getsize("input.txt") == os.path.getsize("output.txt"):
            print(x + ": No significant change!")
            w(x + ":No significant change!")

        else:
            print(x + ": No cleaning done!")
            w(x + ":No cleaning done!")
        os.remove("input.txt")
        os.remove("output.txt")

    if mode == "n":
        wait()
        if os.path.exists("log"):
            os.remove("log")


# Function to remove metadata of all images (filetype = i) or videos (filetype = v) from folder.
def bulk(filetype):
    start()
    loc = input(" Enter Folder: ")
    os.chdir(loc)
    for i in os.listdir():
      singly(i, filetype, "b")
      clear()

    print("\nOutput\n")
    
    if os.path.exists("log"):
        display("log")
        os.remove("log")
    else:
      if filetype == "i":
        print("No Image Files Detected!")
      elif filetype == "v":
        print("No Video Files Detected!")
    print("Done")
    wait()
    end()

if __name__ == "__main__":
    print("\n ┣━━━━━ MRT module stable release version 0.2.4 ━━━━━┫")
    wait()
