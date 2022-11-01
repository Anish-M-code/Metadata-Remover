#flag=imp

from metadata_remover.commons import cls, exiftool, wait
from metadata_remover.mrt import bulk, bulk1, singly, meta

import os
from shutil import move,copy

# Display menu
cls()
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
match x:
    case '1':
        file=input('\n Enter image name:')
        singly(file,'i')
    case '2':
        file=input('\n Enter Video name:')
        singly(file,'v')
    case '3':
        file=input('\n Enter Audio File:')
        y=copy(file,'MRT')
        os.chdir('MRT')
        os.system('py mat2.py '+file)
        y=move(file.split('.')[0]+'.cleaned.'+file.split('.')[1],'..')
        os.remove(file)
        os.chdir('..')
    case '4':
        file=input('\n Enter Torrent File:')
        y=copy(file,'MRT')
        os.chdir('MRT')
        os.system('py mat2.py '+file)
        y=move(file.split('.')[0]+'.cleaned.'+file.split('.')[1],'..')
        os.remove(file)
        os.chdir('..')
    case '5':
        bulk()
    case '6':
        bulk1()
    case '7':
        exiftool()
        rb=input(' Enter Filename:')
        if os.path.exists(rb)==False:
            print('\n File Not Found!\n')
            wait()
            exit(0)
        meta(rb)
        wait()
exit()