#flag=imp

''' An Cross-platform opensource Metadata Remover using exiftool and ffmpeg to sanitize your images before posting on internet.'''

try:
  
  from commons import *
  
except ImportError:
  print(" The commons Modules Not Found! in mrt")
  x=input()
  exit()

def w(msg,file='log'):
    with open(file,'a+') as f:
      f.write('\n'+msg)

#Function to store metadata of file in meta.txt using exiftool.  
def meta(file):
  os.system('exiftool '+file+' >meta.txt')
  display('meta.txt')
  os.remove('meta.txt')

#Function to rename exiftool(-k).exe to exiftool.exe
def autoexif():
 if os.path.exists("exiftool(-k).exe"):
   try:
     os.rename('exiftool(-k).exe','exiftool.exe')
   except FileExistsError:
     print("Exiftool Already Exists!...\n")

#Function to sanitize images using exiftool.
def img(x):
  os.system("exiftool "+x+" -all=")
 
#Function to sanitize videos using ffmpeg. 
def vid(x):
  ffmpeg()
  count=-1
  for i in x :
    count+=1
    if x[count]=='.':
      break
  file=x[:count]
  ext=x[count:]
  y=file+'_clean'+ext
  os.system('ffmpeg -i '+x+' -map_metadata -1 -c:v copy -c:a copy '+y)
  if platform.system().lower()=='windows':
    os.system('cls')
  else:
    os.system('clear')
  os.system('exiftool '+y+'>output.txt')
  copy('output.txt','output_log.txt')
 
#Function to clean single image/video file. 
def singly(x,y,mode='n'):
 exiftool()
 autoexif()
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
      copy('input.txt','input_log.txt')
      img(x)
      flag=1
      os.system("exiftool "+x+">output.txt")
      copy('output.txt','output_log.txt')

 elif y.lower()=='v':
   ffmpeg()
   v=('.mp4','.mov','.webm','.ogv','.flv','.wmv','.avi','.mkv','.vob','.ogg','.3gp')
   for i in v:
    if x.lower().endswith(i):   
      os.system("exiftool "+x+">input.txt")
      copy('input.txt','input_log.txt')
      vid(x)
      flag=1
    

 else:
   print(' Unsupported File Format!')
   return 0

 if mode=='n':

  if flag==0:
    print("\n Invalid File for processing!")
    wait()
    exit()

 if ((os.path.exists('input.txt')==True)and(os.path.exists('output.txt')==True)):
  if os.path.getsize('output.txt')==0:
    if platform.system().lower()=='windows':
      os.system('cls')
    else:
      os.system('clear')
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
    wait()
    if os.path.exists('log'):
      os.remove('log')

#Function to sanitize all images in a given folder.    
def bulk():
  start()
  loc=input(' Enter Folder:')
  if platform.system().lower()=='windows':
    if os.path.exists('exiftool.exe'):
      bcopy('exiftool.exe',loc+'\\exiftool.exe')
  os.chdir(loc)
  for i in os.listdir():
      singly(i,'i','b')
      if platform.system().lower()=='windows':
         os.system('cls')
      else:
         os.system('clear')
  
  print('\nOutput\n')       
  display('log')
  if os.path.exists('log'):
    os.remove('log')
  else:
    print('No Image Files Detected!')
  print('Done')
  wait()
  end()

#Function to sanitize all videos in a given folder.
def bulk1():
  start()
  loc=input(' Enter Folder:')
  if platform.system().lower()=='windows':
    if os.path.exists('exiftool.exe'):
      bcopy('exiftool.exe',loc+'\\exiftool.exe')
    if os.path.exists('ffmpeg.exe'):
      bcopy('ffmpeg.exe',loc+'\\ffmpeg.exe')
  os.chdir(loc)
  for i in os.listdir():
      singly(i,'v','b')
      if platform.system().lower()=='windows':
         os.system('cls')
      else:
         os.system('clear')
  print('\nOutput\n')
  display('log')
  if os.path.exists('log'):
    os.remove('log')
  else:
    print('No Video Files Detected!')
  wait()
  end()
    
      
if __name__=='__main__':
  print('\n |----- MRT module stable release version 0.2.4 ----|')
  wait()

  
    
   
   
