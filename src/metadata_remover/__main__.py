#flag=imp

from metadata_remover import commons
from metadata_remover import mrt

import os
from shutil import move,copy

# Clearscreen
if platform.system().lower()=='windows':
    os.system('cls')
else:
    os.system('clear')

# Display menu
print('''
\n |------ Metadata Removal Tool ------|\n
    1)Remove Metadata from a image.
    2)Remove Metadata from a video.
    3)Remove Metadata from a audio.
    4)Remove Metadata from a Torrent.
    5)Remove Metadata from all images in folder.
    6)Remove Metadata from all videos in folder.
    7)View Metadata in a file.
''')

# Take and parse input
x=input('\n Enter command(1,2,3,4,5,6 or 7):')
if x=='1':
    file=input('\n Enter image name:')
    singly(file,'i')
    exit()
elif x=='2':
    file=input('\n Enter Video name:')
    singly(file,'v')
    exit()
elif x=='3':
    file=input('\n Enter Audio File:')
    y=copy(file,'MRT')
    os.chdir('MRT')
    os.system('py mat2.py '+file)
    y=move(file.split('.')[0]+'.cleaned.'+file.split('.')[1],'..')
    os.remove(file)
    os.chdir('..')
    exit()
elif x == '4':
    file=input('\n Enter Torrent File:')
    y=copy(file,'MRT')
    os.chdir('MRT')
    os.system('py mat2.py '+file)
    y=move(file.split('.')[0]+'.cleaned.'+file.split('.')[1],'..')
    os.remove(file)
    os.chdir('..')
    exit()
elif x=='5':
    bulk()
    exit()
elif x=='6':
    bulk1()
    exit()
elif x=='7':
    exiftool()
    rb=input(' Enter Filename:')
    if os.path.exists(rb)==False:
        print('\n File Not Found!\n')
        wait()
        exit(0)
    meta(rb)
    wait()
    exit()
elif x.lower()=='mm' or x.lower()=='c' or x.lower()=='close':
    exit()
else:
    exit()