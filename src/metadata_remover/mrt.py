#flag=imp

''' 
A Cross-platform opensource Metadata Remover using exiftool and ffmpeg to sanitize your images before posting on internet.
'''

import os, time
import metadata_remover.commons as c
import platform

# Function to write given message to file named log in append mode.
def w(msg,file='log'):
    with open(file,'a+') as f:
      f.write('\n'+msg)

# Function to read and display metadata of a file.  
def meta(file):
  os.system('exiftool '+file+' >meta.txt')
  c.c.display('meta.txt')
  os.remove('meta.txt')

# Function to rename exiftool(-k).exe as exiftool.exe in windows.
def autoexif():
 if os.path.exists("exiftool(-k).exe"):
   try:
     os.rename('exiftool(-k).exe','exiftool.exe')
   except FileExistsError:
     print("Exiftool Already Exists!...\n")
     os.remove("exiftool(-k).exe")

# Function to remove metadata from image file.
def img(x):
  os.system("exiftool "+x+" -all=")

# Function to remove metadata from video file. 
def vid(x):
  c.ffmpeg()
  count=-1
  for i in x :
    count+=1
    if x[count]=='.':
      break
  file=x[:count]
  ext=x[count:]
  y=file+'_clean'+ext
  os.system('ffmpeg -i '+x+' -map_metadata -1 -c:v copy -c:a copy '+y)
  c.cls()
  os.system('exiftool '+y+'>output.txt')
  c.copy('output.txt','output_log.txt')

# Function to remove metadata from single image or video file. It uses img() and vid() internally.
# x denotes file given as input , y can be either i for images or v for videos , mode can be n for normal mode, or b for bulk processing mode.
def singly(x,y,mode='n'):
 autoexif()
 c.exiftool()
 flag=0

 if os.path.exists(x)==False:
   print("File Doesn't Exist!\n")
   time.sleep(3)
   exit(0)
   
 # should include function detect to detect exiftool [imp]
 if y.lower()=='i':
   v=('.jpg','.gif','.bmp','.tiff','.jpeg','.png')
   for i in v:
    if x.lower().endswith(i):   
      os.system("exiftool "+x+">input.txt")
      c.copy('input.txt','input_log.txt')
      img(x)
      flag=1
      os.system("exiftool "+x+">output.txt")
      c.copy('output.txt','output_log.txt')

 elif y.lower()=='v':
   c.ffmpeg()
   v=('.mp4','.mov','.webm','.ogv','.flv','.wmv','.avi','.mkv','.vob','.ogg','.3gp')
   for i in v:
    if x.lower().endswith(i):   
      os.system("exiftool "+x+">input.txt")
      c.copy('input.txt','input_log.txt')
      vid(x)
      flag=1
    
 else:
   print(' Unsupported File Format!')
   return 0

 if mode=='n':

  if flag==0:
    print("\n Invalid File for processing!")
    c.wait()
    exit()

 if ((os.path.exists('input.txt')==True)and(os.path.exists('output.txt')==True)):
  if os.path.getsize('output.txt')==0:
    c.cls()
    print(' Error Processing File!')
  elif os.path.getsize('input.txt')>os.path.getsize('output.txt'):
    print(x+': Metadata removed successfully!')
    w(x+': Metadata removed successfully!')
  elif os.path.getsize('input.txt')==os.path.getsize('output.txt'):
    print(x+": No significant change!")
    w(x+':No significant change!')
    
  else:
    print(x+": No cleaning done!")
    w(x+':No cleaning done!')
  os.remove('input.txt')
  os.remove('output.txt')
      
 if mode=='n':
    c.wait()
    if os.path.exists('log'):
      os.remove('log')

# Function to remove metadata of all images from folder.    
def bulk():
  c.start()
  loc=input(' Enter Folder:')
  if platform.system().lower() == 'windows' =='windows':
    if os.path.exists('exiftool.exe'):
      c.copy('exiftool.exe',loc+'\\exiftool.exe')
  os.chdir(loc)
  for i in os.listdir():
      singly(i,'i','b')
      c.cls()
  
  print('\nOutput\n')       
  c.display('log')
  if os.path.exists('log'):
    os.remove('log')
  else:
    print('No Image Files Detected!')
  print('Done')
  c.wait()
  c.end()

# Function to remove metadata of all videos from folder.
def bulk1():
  c.start()
  loc=input(' Enter Folder:')
  if platform.system().lower() == 'windows' =='windows':
    if os.path.exists('exiftool.exe'):
      c.copy('exiftool.exe',loc+'\\exiftool.exe')
    if os.path.exists('ffmpeg.exe'):
      c.copy('ffmpeg.exe',loc+'\\ffmpeg.exe')
  os.chdir(loc)
  for i in os.listdir():
      singly(i,'v','b')
      c.cls()
  print('\nOutput\n')
  c.display('log')
  if os.path.exists('log'):
    os.remove('log')
  else:
    print('No Video Files Detected!')
  c.wait()
  c.end()
      
if __name__=='__main__':
  print('\n |----- MRT module stable release version 0.2.4 ----|')
  c.wait()
