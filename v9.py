#flag=imp

try:
    from commons import *
    from mrt import *
    from emrt import *
   
    
except ImportError:
    print(' Critical Error :Required Modules were not Found!')
    x=input('\n Press any key to exit...')
    exit()


def san():
    cls()
    print('\n |------ Metadata Removal Tool ------|\n')
    print(' 1)Remove Metadata from images.')
    print(' 2)Remove Metadata from videos.')
    print(' 3)Bulk Image Metadata Removing Script Generator.')
    print(' 4)Remove Metadata from all images in folder.')
    print(' 5)Remove Metadata from all videos in folder.')
    print(' 6)View Metadata in a file.')
    x=input('\n Enter command(1,2,3,4,5 or 6):')
    if x=='1':
        file=input('\n Enter image name:')
        singly(file,'i')
        san()
        exit()
    elif x=='2':
        file=input('\n Enter Video name:')
        singly(file,'v')
        san()
        exit()
    elif x=='3':
        bulkimgScript()
        san()
        exit()
    elif x=='4':
        bulk()
        san()
        exit()
    elif x=='5':
        bulk1()
        san()
        exit()
    elif x=='6':
        exiftool()
        rb=input(' Enter Filename:')
        if os.path.exists(rb)==False:
            print('\n File Not Found!\n')
            wait()
            san()
            exit(0)
        meta(rb)
        wait()
        san()
        exit()
    elif x.lower()=='mm':
        san()
    elif x.lower()=='c' or x.lower()=='close':
        exit()
    else:
        san()

san()