#flag=imp

''' 
This is the common library developed to satisfy the needs of  commandline python applications .
It contains necessary  std libraries and basic functions for  its users.
'''	
	
import platform
import os
import webbrowser

# Deletes file after checking if it exists or not.
def r(f):
   if os.path.exists(f):
      os.remove(f)

# Function to open website if prerequisite software is not found in PC.    
def detect(cmd,web,snam,pkg):
        cls()
    
        if sys() =='windows':
              if os.system(cmd+'>chk')!=0:
                print('\nError: '+pkg+' is not detected!')
                print('\nPlease wait opening '+snam +' website in your browser!\nYou Have to download and install it.\n')
                webbrowser.open(web)
                x=input('\nPress any key to exit...')
                r('chk')
                exit()
                
        else:
         if os.system(cmd+'>chk')!=0:      
           print('\nError:'+pkg+' is not detected!\n Please install The package to continue.')
           x=input('\nPress any key to exit...')
           r('chk')
           exit()
        r('chk')
           

def start():
    print('\n<-----Task Started----->\n')
    
def end():
    print('\n<-----Task Completed----->\n')

def tsks():
    start()
    
def tske():
    end()

def tskf():
    print('\n<-----Task Failed !----->\n')


def wait():
      x=input('\nPress any key to continue...\n')

# Function to Display contents of text file.
def display(file):
        with open(file,'r') as f:
            s=f.read(1024)
            print(s)
            while len(s)>0:
                s=f.read(1024)
                print(s)
    

def gpg():
   detect('gpg --version','https://gpg4win.org','gpg4win','Gnupg')
   
  
def exiftool():
   detect('exiftool -h','https://exiftool.org','exiftool','Exiftool')

def ffmpeg():
   detect('ffmpeg --help','https://ffmpeg.org/','ffmpeg','ffmpeg')

# Function to copy textfile.
def copy(file,file1):
   if os.path.exists(file):
    f=open(file,'r')
    s=open(file1,'a+')
    if os.path.getsize(file)<(1024*1024*1024):
      buff=f.read()
      s.write('\n-------------------------------------------------------\n')
      s.write(buff)
    f.close()
    s.close()

# Function to copy binaryfile.
def bcopy(file,file1):
   if os.path.exists(file):
    f=open(file,'rb')
    s=open(file1,'ab+')
    if os.path.getsize(file)<(1024*1024*1024):
      buff=f.read()
      s.write(buff)
    f.close()
    s.close()

# Clear screen
def cls():
    os.system('cls') if sys() == 'windows' else os.system('clear')

# Get system name
def sys():
    return "windows" if platform.system().lower() == 'windows' else "notwin"
