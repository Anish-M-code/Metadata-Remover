#flag=imp
#[ stable release ] 

''' This module contains all the functions for simply encrypt
    project '''
try:
    import os
    import getpass
    import secrets
except ImportError:
    print('Critical Error: Required Modules Not found!\n')
    x=input('Press any key to continue...')
    exit(1)

A=((0,'A'),(1,'B'),(2,'C'),(3,'D'),(4,'E'),(5,'F'),(6,'G'),(7,'H'),(8,'I'),(9,'J'),(10,'K'),(11,'L'),(12,'M'),(13,'N'),(14,'o'),(15,'P'),(16,'Q'),(17,'R'),(18,'S'),(19,'T'),(20,'U'),(21,'V'),(22,'W'),(23,'X'),(24,'Y'),(25,'Z'),(26,'0'),(27,'1'),(28,'2'),(29,'3'),(30,'4'),(31,'5'),(32,'6'),(33,'7'),(34,'8'),(35,'9'))
A=list(A)
secrets.SystemRandom().shuffle(A)
A=tuple(A)

#converts Alphanumeric characters to numbers of base 36    
def f(x):
  store=[]
  for s in x:
    count=0
    for i in range(36):
        if A[i][1].lower()==s.lower():
          store.append(A[i][0])
          count=1
          break
    if count==0:
      store.append(' ')
  return tuple(store)                
    
#converts base 36 numbers to alphanumeric charactors.
def rf(x):
  store=[]
  q=''
  for s in x:
    count=0
    for i in range(36):
        if A[i][0]==s:
          store.append(A[i][1])
          count=1
          break
    if count==0:
      store.append(' ')
  q=''.join(store)
  return q
    
#generates key with keyfile.        
def key(x):
    seed=list(range(36))
    masterkey=[]
    for i in range(len(x)):
        masterkey.append(secrets.choice(seed))
    if os.path.exists('key'):
        print('This program has detected a key!\n')
        n=input('Enter a new name for your old key!')
        if len(n)==0:
            n='oldkey'
        os.rename('key',n)
    with open('key','w') as fp:
        fp.write(rf(masterkey))

#generates encrypted file for given message(msg).
def encrypt(msg,output='msg.cry',k='key'):
    ciphertxt=[]
    x=f(msg)
    key(msg)
    buff=''
    if os.path.exists(k)==False:
        print('Keyfile not found!')
        feed=input('\nPress any key to continue...')
        exit(1)
    with open(k,'r') as fp:
        buff=fp.readline().strip()
    y=f(buff)
    if len(x)<=len(buff):
        for i in range(len(x)):
            if type(x[i])==int and type(y[i])==int:
                ciphertxt.append(((x[i]+y[i])%36))
            else:
                ciphertxt.append(' ')
    else:
        print('\nThe length of message is greater than the key!')
        tskf()
        x=input('Press any key to continue...')
        exit(1)
    ciphertxt=tuple(ciphertxt)
    ctxt=rf(ciphertxt)
    if os.path.exists(output):
        print('\n'+output+' already exists..')
        dog=input('Enter a name to rename this file:')
        os.rename(output,dog)
    with open(output,'w') as fp:
        fp.write(ctxt)
    display(output)

#decrypts a given encrypted file and stores plaintxt in a file which is passed in out parameter.   
def decrypt(file='msg.cry',out='output.txt',k='key'):
    ptxt=[]
    buff=''
    mem=''
    
    if os.path.exists(k)==False:
        print('Error:Keyfile not found!')
        tskf()
        wait()
        exit(1)
    if os.path.exists(file)==False:
        print('Error:The Encrypted File '+file+' is not found!')
        tskf()
        wait()
        exit(1)
    with open(k,'r') as fp:
        buff=fp.readline().strip()
    y=f(buff)
    with open(file,'r') as fl:
       mem=fl.readline().strip()
    x=f(mem)
    if len(x)<=len(buff):
        for i in range(len(x)):
            if type(x[i])==int and type(y[i])==int:
                ptxt.append(((x[i]-y[i])%36))
            else:
                ptxt.append(' ')
    ptxt=tuple(ptxt)
    plaintxt=rf(ptxt)
    if os.path.exists(out):
        print('\n'+out+' already exists..')
        dog=input('Enter a name to rename this file:')
        os.rename(out,dog)
    with open(out,'w') as fp:
        fp.write(plaintxt)
    display(out)

#generates a key without keyfile.
def ikey(x):
    seed=list(range(36))
    masterkey=[]
    for i in range(len(x)):
        masterkey.append(secrets.choice(seed))
    m=tuple(masterkey)
    return m

#encrypts a given string and returns ciphertxt and key as a tuple. (no file generated!)
def en(msg):
    ciphertxt=[]
    x=f(msg)
    y=ikey(msg)
    if len(x)<=len(y):
        for i in range(len(x)):
            if type(x[i])==int and type(y[i])==int:
                ciphertxt.append(((x[i]+y[i])%36))
            else:
                ciphertxt.append(' ')
    else:
        x=input('Press any key to continue...')
        exit(1)
    ciphertxt=tuple(ciphertxt)
    ctxt=rf(ciphertxt)
    shk=rf(y)
    return (ctxt,shk)

#decrypts a given encrypted string and returns a plaintxt as output.
def de(c,k):
    ciphertxt=[]
    x=f(c)
    y=f(k)
    if len(x)<=len(y):
        for i in range(len(x)):
            if type(x[i])==int and type(y[i])==int:
                ciphertxt.append(((x[i]-y[i])%36))
            else:
                ciphertxt.append(' ')
    else:
        x=input('Press any key to continue...')
        exit(1)
    ciphertxt=tuple(ciphertxt)
    ctxt=rf(ciphertxt)
    return (ctxt)

#function for secret splitting interface.
def sprocess():
    table=[]
    print('''\n         ---------------------------------------------------------
               |            Secret splitting                   |
         -----------------------------------------------------------''')
    while(1):
        try:
            x=int(input('\nEnter the number of shares(atmost 10):'))
            if(x<11)and(x>1):
                break
        except ValueError:
            print('\nPlease enter a valid integer greater than 1 but less than or equal to 10!\n')
    msg=getpass.getpass('Enter the secret:')
    table+=list(en(msg))
    for i in range(2,x):
        tmp=table[-1]
        table.pop()
        table+=list(en(tmp))
    for i in range(len(table)):
        print('SHARE',i+1,':',table[i])

#function for secret combining interface.
def cprocess():
    table=[]
    print('''\n          ---------------------------------------------------------
                |          Secret Combine                     |
          -----------------------------------------------------------''')
    while(1):
        try:
            x=int(input('\nEnter no. of shares to combine(atmost 10):'))
            if(x<11)and(x>1):
                break
        except ValueError:
                print('\nPlease enter a valid integer greater than 1 but less than or equal to 10!\n')
    for i in range(x):
            table.append(getpass.getpass(str('Enter Share '+str(i+1)+':')))
    for i in range(x-1):
            hook=[]
            a,b=table[-2],table[-1]
            table.pop()
            table.pop()
            hook.append(de(a,b))
            table+=hook
    print()
    print(''.join(table))
        

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

def display(file):
        if os.path.exists(file)==False:
           print('Error: '+file+' not found!')
           wait()
           exit(1)
        with open(file,'r') as f:
            s=f.read(1024)
            print(s)
            while len(s)>0:
                s=f.read(1024)
                print(s)

# function for main interface.    
def mm():
   print('''\n         ------------------------------------------------------------------
               |              Simply Encrypt!                         |
           ---------------------------------------------------------------''')
   print('\n1)Encrypt a message')
   print('2)Decrypt a message')
   print('3)Secret splitting')
   print('4)Secret combine')
   cmd=input('\nEnter command:')
   if cmd=='1':
      emu()
      mm()
   elif cmd=='2':
      dmu()
      mm()
   elif cmd=='3':
       process()
       mm()
   elif cmd=='4':
       rprocess()
       mm()
   elif cmd.lower()=='c' or cmd.lower()=='close':
      exit()
   else:
      print('please enter 1 or 2 or \'c to exit!')
      mm()
   exit()

#function for encryption interface.      
def emu():
    
   print('''\n         -------------------------------------------------------------------
                 |            Encryption Menu                         |
            ----------------------------------------------------------------''')
   print('\n1)Encrypt a message in this prompt.')
   print('2)Encrypt a text file containing message.')
   cmd=input('\nEnter command:')
   if cmd=='1':
      esm()
   elif cmd=='2':
      esm2()
   elif cmd.lower()=='c' or cmd.lower()=='close':
      exit()
   elif cmd.lower()=='mm':
      mm()
      exit()
   else:
      print('please enter 1 ,2 or c to close or mm for main menu!')
      emu()
   exit()
   
def esm():
   msg=getpass.getpass('\nEnter msg:')
   fil=input('Enter output filename( contains ciphertxt):')
   start()
   if len(fil)==0:
      encrypt(msg)
   else:
      encrypt(msg,fil)
   end()
   wait()
   emu()

def esm2():
   
   print('''\nWarning if your file contains characters other than alphabets
              or numbers it may be lost forever!\n''')
   fil=input('\nEnter Filename containing message:')
   if os.path.exists(fil)==False:
      print('Error: '+fil+' not found!')
      wait()
      emu()
      exit()
   with open(fil,'r') as fp:
      msg=fp.readline().strip()
      m=msg
      while len(msg)>0:
         msg=fp.readline().strip()
         m+=msg
   out=input('Enter output filename( contains ciphertxt):')
   start()
   if len(out)==0:
      encrypt(m)
   else:
      encrypt(m,out)
   end()
   wait()
   emu()
   exit()

#function for decryption interface.
def dmu():
   print('''\n           --------------------------------------------------------------
                  |          Decryption Menu                   |
            --------------------------------------------------------------''')
   fil=input('\nEnter Filename containing ciphertext:')
   if os.path.exists(fil)==False:
      print('Error: '+fil+' not found!')
      wait()
      dmu()
      exit()
   skey=input('\nEnter Filename containing key(default: \'key\'):')
   if len(skey)==0:
      skey='key'
   with open(fil,'r') as fp:
      msg=fp.readline().strip()
      m=msg
      while len(msg)>0:
         msg=fp.readline().strip()
         m+=msg
   out=input('Enter output filename( contains plaintxt):')
   start()
   if len(out)==0:
      out='output.txt'
      decrypt(fil,out,skey)
   else:
      decrypt(fil,out,skey)
   end()
   wait()
   mm()
   exit()


    
   
        
        
