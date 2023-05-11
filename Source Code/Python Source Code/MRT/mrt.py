# flag=imp

'''Functions used: 
wait (from commons) 
writeMessage
metaView
writeToInputOutput
removeImageMetadata
removeVideoMetadata
autoexif
mainFunc
bulk
cls (from commons)
copyFile (from commons)
'''

""" 
A Cross-platform open source Metadata Remover using exiftool and ffmpeg to sanitize your images before posting on internet.
"""

try:
  from commons import *
except ImportError:
  print("The \"commons\" module was not found.")
  input("Press any key to exit...")
  exit()

# Function to write given message to file named log in append mode.
def writeMessage(msg, file="log"):
  with open(file, "a") as f:
    f.write("\n" + msg)

# Function to read and display metadata of a file.
def metaView(file):
  if OS:
    os.system(os.path.join(cwd,"exiftool ") + file + " > meta.txt")
  else:
    os.system("exiftool " + file + " > meta.txt")
  printFile("meta.txt")
  os.remove("meta.txt")


# Function to rename exiftool(-k).exe as exiftool.exe in windows.
def autoexif():
  if os.path.exists("exiftool(-k).exe"):
    try:
      os.rename("exiftool(-k).exe", "exiftool.exe")
    except FileExistsError:
      # I don't think it is relevant for the user to know that it has been renamed, and maybe 
      # we shouldn't go around messing with people's installations, but I'm leaving this here
      os.remove("exiftool(-k).exe")

# Save the current working directory that the executables are in
cwd = os.getcwd()

# Write either input log (i) or output log (o) using correct executable filepath.
# This deprecates old bcopy() function which copied the binary into the working directory for windows

# (9x14S): changed the two if statements (need exclusion of the other if one is executed) to if-elif-
# else statements with a final raise exception statement to give an error
def writeToInputOutput(x, mode='i'):
  if mode == 'i':
    modeName = "input"
  elif mode == "o":
    modeName = "output"
  else:
    raise ValueError("Unknown mode for writeToInputOutput (has to be either 'o' or 'i') in mrt")
  if OS:
      os.system(os.path.join(cwd,"exiftool ") + x + "> {}.txt".format(modeName))
  else:
      os.system("exiftool " + x + "> {}.txt".format(modeName))

# Function to remove metadata from image file.
def removeImageMetadata(imageFile):
  if imageFile.lower().endswith(".tiff") or imageFile.lower().endswith(".tif"):
    if OS:
      os.system(os.path.join(cwd,"exiftool -all=  ") + imageFile)
      return
    else:
      os.system("exiftool -all=  " + imageFile)
      return
  else:
    raise ValueError("Bad imageFile data in variable argument for removeImageMetadata in mrt")

# Function to remove metadata from video file.
def removeVideoMetadata(videoFile):
  # ffmpeg()
  # videoFile is a string, so access the index of the dot with the index() method instead of 
  # iterating over every character
  count = videoFile.index(".")
  file = videoFile[:count]
  ext = videoFile[count:]
  y = file + "_clean" + ext
  if OS:
    os.system(os.path.join(cwd,"ffmpeg -i ") + videoFile + " -map_metadata -1 -c:v copy -c:a copy " + y)
  else:
    os.system("ffmpeg -i " + videoFile + " -map_metadata -1 -c:v copy -c:a copy " + y)
  cls()
  writeToInputOutput(y,'o')
  copyFile("output.txt", "output_log.txt")

# Function to remove metadata from single image or video file. It uses img() and 
# removeVideoMetadata() internally.

# file denotes file given as input, typeOfFile can be either i for images or v for videos, its else 
# block raises an error,
# mode can be True for normal (single) mode, or False for bulk processing mode.
def mainFunc(file, typeOfFile, mode=True):
  autoexif()
  flag = 0
  if not os.path.exists(file):
    print("File doesn't exist.")
    time.sleep(3)
    exit(0)
  # should include function detect to detect exiftool [imp]
  if typeOfFile == "i":
    v = (".jpg", ".gif", ".bmp", ".tiff", ".jpeg", ".png", ".tif")
    for i in v:
      if file.lower().endswith(i):
        writeToInputOutput(file,'i')
        copyFile("input.txt", "input_log.txt")
        removeImageMetadata(file)
        flag = 1
        writeToInputOutput(file,'o')
        copyFile("output.txt", "output_log.txt")

  elif typeOfFile == "v":
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
      ".3gp",)
    for i in v:
      if file.lower().endswith(i):
        writeToInputOutput(file,'i')
        copyFile("input.txt", "input_log.txt")
        removeVideoMetadata(file)
        flag = 1

  else:
    print(" Unsupported File Format!")
    return 0

  if mode:
    if os.path.exists("log"):
      os.remove("log")
    if not flag:
      print("\n Invalid File for processing!")
      wait()

  if (os.path.exists("input.txt")) and (os.path.exists("output.txt")):
    if not os.path.getsize("output.txt"):
      cls()
      print("Error Processing File!")
    elif os.path.getsize("input.txt") > os.path.getsize("output.txt"):
      print(file + ": Metadata removed successfully!")
      writeMessage(file + ": Metadata removed successfully!")
    elif os.path.getsize("input.txt") == os.path.getsize("output.txt"):
      print(file + ": No significant change!")
      writeMessage(file + ":No significant change!")
    else:
      print(file + ": No removal has been done!")
      writeMessage(file + ": No removal has been done!")
    os.remove("input.txt")
    os.remove("output.txt")

# Function to remove metadata of all images (filetype = i) or videos (filetype = v) from folder.
def bulk(fileType):
  loc = input("Enter Folder: ")
  taskStart()
  os.chdir(loc)
  for i in os.listdir():
    mainFunc(i, fileType, True)
    cls()

  print("\nOutput: \n")
  
  if os.path.exists("log"):
      printFile("log")
      os.remove("log")
  else:
    if fileType == "i":
      print("No Image Files Detected!")
    elif fileType == "v":
      print("No Video Files Detected!")
  print("Done")
  wait()
  taskEnd()

if __name__ == "__main__":
  print("\n |----- MRT module stable release version 0.2.4 ----|")
  wait()
