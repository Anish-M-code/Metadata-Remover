try:
  from commons import *
except ImportError:
  print('commons Module not Found in emrt!')
  x=input()
  exit()

# This is a extension for mrt module 0.1 

# Function to generate batch/shell script to remove metadata from common image files.
def bulkimgScript():
  ext=input("\nEnter Image's Extension:")
  if ext[0]!='.':
      ext='.'+ext
  if ext not in ('.jpg','.gif','.bmp','.tiff','.jpeg','.png'):
      print('\nInvalid Filename!')
      wait()
      exit()
  if platform.system().lower()=='windows':
      with open('runscript.bat','w') as f:
          f.write('echo off\nexiftool *'+ext+'>input.txt\n')
          f.write('exiftool -all= *'+ext)
          f.write('\nexiftool *'+ext+'>output.txt\npause')
          print('\nScript Generated Successfully!')
          wait()

  elif platform.system().lower()=='linux':
      with open('runscript.sh','w') as f:
          f.write('exiftool *'+ext+'>input.txt\n')
          f.write('exiftool -all= *'+ext)
          f.write('\nexiftool *'+ext+'>output.txt\n')
          print('\nScript Generated Successfully!')
          wait()
          
if __name__=='__main__':
    print('\nExtension of MRT module\n')
    print('\nCompatible with all commons module versions!')
    print('Extension developed by Fixit Project')  
    wait()
