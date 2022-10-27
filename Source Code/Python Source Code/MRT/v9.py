#flag=imp

try:
    from commons import *
    from mrt import *
   
except ImportError:
    print(' Critical Error :Required Modules were not Found!')
    x=input('\n Press any key to exit...')
    exit()

import os
from shutil import move,copy
try:
    import mutagen
except:
    os.system('pip install mutagen')

# Function to display main menu()
def san():
    cls()
    print('\n |------ Metadata Removal Tool ------|\n')
    print(' Please select an option from the following:')
    print(' 1)Remove Metadata from a image.')
    print(' 2)Remove Metadata from a video.')
    print(' 3)Remove Metadata from a audio.')
    print(' 4)Remove Metadata from a Torrent.')
    print(' 5)Remove Metadata from all images in folder.')
    print(' 6)Remove Metadata from all videos in folder.')
    print(' 7)View Metadata in a file.')
    print(' c)Close.')
    x=input('\n Enter command(1,2,3,4,5,6,7 or c):')
    if x=='1':
        file=input('\n Enter image name:')
        singly(file,'i')
    elif x=='2':
        file=input('\n Enter Video name:')
        singly(file,'v')
    elif x=='3':
        file=input('\n Enter Audio File:')
        y=copy(file,'MRT')
        os.chdir('MRT')
        os.system('py mat2.py '+file)
        y=move(file.split('.')[0]+'.cleaned.'+file.split('.')[1],'..')
        os.remove(file)
        os.chdir('..')
    elif x == '4':
        file=input('\n Enter Torrent File:')
        y=copy(file,'MRT')
        os.chdir('MRT')
        os.system('py mat2.py '+file)
        y=move(file.split('.')[0]+'.cleaned.'+file.split('.')[1],'..')
        os.remove(file)
        os.chdir('..')
    elif x=='5':
        bulk()
    elif x=='6':
        bulk1()
    elif x=='7':
        exiftool()
        rb=input(' Enter Filename:')
        if os.path.exists(rb)==False:
            print('\n File Not Found!\n')
            wait()
            san()
            exit(0)
        meta(rb)
        wait()
    elif x.lower()=='c' or x.lower()=='close':
        exit()

while(True):
    san()
