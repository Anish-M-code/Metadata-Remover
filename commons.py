#flag=imp

''' This is the common library developed to satisfy the needs of  commandline python applications .
    It contains necessary  std libraries and basic functions for  its users.'''
	
	
try:
   import hashlib
   import time
   import platform
   import os
   import getpass
   import webbrowser

except ImportError:
    print('Critical Error:Necessary Python Modules are missing!')
    print('Commons module couldnot satisfy all the dependencies!')
    x=input('\nPress any key to exit...')
    exit()

#Function to remove a file if it exists.
def r(f):
   if os.path.exists(f):
      os.remove(f)
 
#Function to detect if required tools/package is present on local host or not. 
def detect(cmd,web,snam,pkg):
    
        if platform.system().lower()=='windows':
              if os.system(cmd+'>chk')!=0:
                os.system('cls')
                print('\nError: '+pkg+' is not detected!')
                print('\nPlease wait opening '+snam +' website in your browser!\nYou Have to download and install it.\n')
                webbrowser.open(web)
                x=input('\nPress any key to exit...')
                r('chk')
                exit()
                
        else:
         if os.system(cmd+'>chk')!=0:  
           os.system('clear')         
           print('\nError:'+pkg+' is not detected!\n Please install The package to continue.')
           x=input('\nPress any key to exit...')
           r('chk')
           exit()
        r('chk')
           

#Function to notify user that task has started.
def start():
    print('\n<-----Task Started----->\n')
 
#Function to notify user that task has ended. 
def end():
    print('\n<-----Task Completed----->\n')

#Alias for start()
def tsks():
    start()
  
#Alias for end()  
def tske():
    end()

#Function to notify user that task has failed.
def tskf():
    print('\n<-----Task Failed !----->\n')

#Function to pause program until next user input.
def wait():
      x=input('\nPress any key to continue...\n')

#Function to display contents of text file.
def display(file):
        with open(file,'r') as f:
            s=f.read(1024)
            print(s)
            while len(s)>0:
                s=f.read(1024)
                print(s)
    
#Function to Detect exiftool on local host.
def exiftool():
   detect('exiftool -h','https://exiftool.org','exiftool','Exiftool')

#Function to Detect ffmpeg tool on local host.
def ffmpeg():
   detect('ffmpeg --help','https://ffmpeg.org/','ffmpeg','ffmpeg')

#Function to copy text file.
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

#Function to copy binary file
def bcopy(file,file1):
   if os.path.exists(file):
    f=open(file,'rb')
    s=open(file1,'ab+')
    if os.path.getsize(file)<(1024*1024*1024):
      buff=f.read()
      s.write(buff)
    f.close()
    s.close()

#Function to clear screen.
def cls():
    if platform.system().lower()=='windows':
       x=os.system('cls')
    else:
       x=os.system('clear')








    
