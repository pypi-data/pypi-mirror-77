'''
This Module is One to Make Your Code Shorter.
High API Will Make You Feel You're Ordering And Machine Is Doing!
Also There is Collection of most usefull function and methods from popular modules of python.
(Read Help of Functions)
Official Documention Will Be Added Soon.
'''
'''
Written By RX
Last Update: 06-01-2020
'''

__version__='2.0.0'


'''
TODO:
- Screen recorder
- Open Video
- Open Audio
- Make Sound
- Smallest and Biggest
- registery editor
'''




#START
import os,random,time,sys
from typing import Any,Iterable,Optional

__all__=['p','repeat','rev',
         'read','write',
         'wait','cls',
         'progressbar',
         'wait_for',
         'call_later',
         'convert_bytes',
         'Input', 'restart_app',
        #Tuples:
         'force','erase',
         'insert','replace',
        #Classes
         'rand','system',
         'File','files',
         'style','record',
         'Tuple'
         ]

#######        8888888888                         888    d8b                                   ####### 
 #####         888                                888    Y8P                                    #####  
  ###          888                                888                                            ###   
   #           8888888 888  888 88888b.   .d8888b 888888 888  .d88b.  88888b.  .d8888b            #    
   #           888     888  888 888 "88b d88P"    888    888 d88""88b 888 "88b 88K                #    
  ###          888     888  888 888  888 888      888    888 888  888 888  888 "Y8888b.          ###   
 #####         888     Y88b 888 888  888 Y88b.    Y88b.  888 Y88..88P 888  888      X88         #####  
#######        888      "Y88888 888  888  "Y8888P  "Y888 888  "Y88P"  888  888  88888P'        ####### 


def p(text='',end='\n'):
    '''
    p is print!
    But because we use it a lot, we\'ve decided to make it one letter.
    Example:
        p('Hello World')
        ==>Hello World
    '''
    print(text,end=end)

def repeat(function,n: int):
    '''
    Repeat function for n times
    for more info see the example below.
    Example:
        repeat(Func_Name, 3)
        ==> "function Func_Name will launch 3 times."
    '''
    i=1
    while i <= n:
        i+=1
        function() 

def rev(var:Any):
    '''
    This function is for reversing Strings, Lists, Tuples And also Integers.
    Example:
        b= rev('Football')
        print(b)
        ==> llabtooF
    '''
    ret=var
    if type(ret)==int or type(ret)==float:
        ret= str(ret)
        ret= ret[::-1]
        if type(var)==int:
            ret= int(ret)
        else:
            ret=float(ret)
    else:
        ret= ret[::-1]
    return ret

def read(file):
    '''
    This can help you to read your file faster.
    Example:
        read_file('C:\\users\\Jack\\test.txt')
        ==> "Content of 'test.txt' will be shown."
    '''
    op= open(file,mode='r')
    FileR= op.read()
    op.close()
    return FileR
def write(file,text='',mode='replace',start=''):
    '''
    With this method you can change content of the file.  
    file:   File you want to change its content.
    content:   Content you want to add to file.
    mode:   Type of writing method.
        'continue' for add content to end of the file. 
        'replace' for overwriting to file content.
    start: I use this when I use mode='continue'
    '''    
    if mode=='replace':
        op= open(file,mode='w')
        op.write(text)
        op.close()
    elif mode=='continue':
        op=open(file,'a')
        op.write(start+str(text))
        op.close() 
    else:   
        print('Error\nmode can only be: 1-replace(default)  2-continue\nNot "{0}"'.format(mode)) 

def wait(seconds):
    '''
    Use this if you want your program wait for a certain time.
    Example:
        wait(3)
        ==> "Nothing happen and there will be no calculation for 3 seconds"
    '''
    time.sleep(seconds)
#__SQ_= 'powernrxbetfromporto'
def cls():
    '''
    You can use this function if you want to clear the environment.
    '''
    import platform
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def progressbar(total=100,dashes_nom=100,delay=1,dashes_shape=' ',complete_shape='█',pre_text='Loading: ',
                left_port='|',right_port='|'):
    '''
    Use this function to make a custom in-app progress bar.
    Example:
        progressbar(Total=100,Dashes_Nom=10,Time=1,Dashes_Shape='-',Complete_Shape='#', Pre_Text='Loading')
        ==>   Loading|####------| 40/100
    '''
    import sys
    def Progressbar(it, prefix="", size=60, file=sys.stdout):
        count = len(it)
        def show(j):
            x = int(size*j/count)
            file.write("%s%s%s%s%s %i/%i\r" % (prefix, right_port, complete_shape*x, dashes_shape*(size-x), left_port, j, count))
            file.flush()        
        show(0)
        for i, item in enumerate(it):
            yield item
            show(i+1)
        file.write("\n")
        file.flush()
    for i in Progressbar(range(total), pre_text, dashes_nom):
        wait(delay)

def wait_for(button):
    '''
    If You Want to Wait For the User to Press a Key (Keyboard or Mouse) Use This Function.
    '''
    if button.lower() in ('middle','left','right','back','forward'):
        if button.lower()[:1]=='b':
            button='x'
        if button.lower()[:1]=='f':
            button='x2'
        import mouse
        mouse.wait(button)
    else:
        import keyboard
        try:
            keyboard.wait(button)
        except:
            raise ValueError('Incorrect Button Name.')

def call_later(function,*args,delay=0.001):
    '''
    Do You Want to Call Your Function Later Even Between Other Operations?
    call_later() will help you to do that!
    First arg should be your function name,
    After That (*args) you can add any args that your function need,
    And Last arg is delay for calling your function in seconds.
    '''
    import keyboard
    keyboard.call_later(function,args,delay)

def convert_bytes(num:int) -> str :
    """
    Convert num to idiomatic byte unit.
    num is the input number (bytes).
    
    >>> convert_bytes(200)
    '200.0 bytes'
    >>> convert_bytes(6000)
    '5.9 KB'
    >>> convert_bytes(80000)
    '78.1 KB'
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def Input(prompt='', default_value=''):
    '''
    Make Default Value For Your Input!  
    (THIS ONLY WORK ON WINDOWS (SORRY))
    prompt is what you want and it's input(prompt) .
    default_value is what there should be after prompt.
    E.g: 
       >>> Input('Is rx7 Library Easy to Learn?  ', 'Yes')
       Is rx7 Library Easy to Learn?  Yes
    '''
    import win32console
    _stdin = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)
    keys = []
    for c in default_value:
        evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
        evt.Char = c
        evt.RepeatCount = 1
        evt.KeyDown = True
        keys.append(evt)
    _stdin.WriteConsoleInput(keys)
    return input(prompt)

def restart_app():
    '''
    This Function Close App and Recall it From Terminal
    '''
    os.system('clear')
    os.execv(sys.executable, ['python'] + sys.argv)    

def active_window_title():
    '''
    Get active windows title  
    (Usually terminal is active window title 
    but if during executing your script if you change window 
    this will return new window title)
    '''
    import pyautogui
    return pyautogui.getActiveWindowTitle()

def open_image(path):
    '''
    Open image file with default image viewer.  
    (Mac OS is not supported yet)
    '''
    import platform
    if platform.system() == 'Windows':
        os.system(str(path))
    elif platform.system() == 'Linux':
        subprocess.getoutput(f'xdg-open {path}')
    else:
        raise OSError('OS X is not supported for this function.')

URL_BASENAME=''
def download(url,filename=URL_BASENAME, save_memory=True, progressbar=True, prefix='Downloading'):
    '''
    Use this function to download files.  
    if filename is not given, it will be last part of the url.  
    filename can be path for saving file.  
    save_memory parameter is used to save memory in large files (save directly to storage)
    '''
    import requests,urllib
    if not filename: filename = url.split('/')[-1]
    pass
    if save_memory:
        '''with urllib.request.urlopen(url) as response, open(filename, 'wb') as f:
            shutil.copyfileobj(response, f)'''
        '''r = requests.get(url, stream = True)
        with open(filename,"wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)'''
        if progressbar:
            with open(filename, "wb") as f:
                response = requests.get(url, stream=True)
                total_length = response.headers.get('content-length')
                if total_length is None:
                    f.write(response.content)
                else:
                    dl = 0
                    done=0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(33 * dl / total_length)
                        sys.stdout.write(f"\r{prefix} {filename}: |{'█' * done}{' ' * (33-done)}| {100-((33-done)*3)}%")
                        sys.stdout.flush()
                    if 100-((33-done)*3) == 96:
                        sys.stdout.write(f"\r{prefix} {filename}: |{'█' * done}{' ' * (33-done)}| 100%")
                        sys.stdout.flush()
        else:
            with open(filename, "wb") as f:
                response = requests.get(url, stream=True)
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)               
    else:
        def report(blocknr, blocksize, size):
            if progressbar:
                current = blocknr*blocksize
                sys.stdout.write("\rDownloading {1}:  {0:.2f}%".format(100.0*current/size,filename))
        def downloadFile(url):
            urllib.request.urlretrieve(url, filename, report)
        downloadFile(url)
    pass
    if progressbar: print()

def extract(filename:str, path:Optional[str]=None,files:Optional[Iterable[str]]=None, password:Optional[str]=None) -> None: 
    '''
    Extract Files from Zip File.\n
    If files parameter is None it will extract all files.\n
    path is path to extract
    '''
    import zipfile
    zipfile.ZipFile(filename, 'r').extractall(path=path,members= files,pwd=password)

def screenshot(image_name='Screenshot.png'):
    '''
    This function will take a screenshot and save it as image_name
    '''
    import pyscreeze
    return pyscreeze.screenshot(image_name)

def func_info(func):

    help(func)
    print('-'*30)
    print('Module  ',func.__module__)
    print('-'*30)
    try:
        _code_ = str(func.__code__)
        _code_= _code_[_code_.index(',')+2:-1]
    except AttributeError:
        _code_ = f'No "file" and "line" information available (I guess "{func}" is a built-in function)'
    print(_code_)

'''
def screen_recorder():
    from screen_recorder_sdk import screen_recorder
    #screen_recorder.enable_dev_log ()
    screen_recorder.disable_log()
    pid = 2456
    screen_recorder.init_resources(pid)
    screen_recorder.start_video_recording ('video1.mp4', 30, 8000000, True)
    time.sleep(10)
    print('hello')
    for i in range(100):
        x= i**3
    screen_recorder.stop_video_recording ()
    screen_recorder.free_resources()

'''




#######         .d8888b.   888  888                                                         #######
 #####         d88P  Y88b  888  888                                                          ##### 
  ###          888    888  888  888                                                           ###  
   #           888         888  888   8888b.   .d8888b   .d8888b    .d88b.   .d8888b           #   
   #           888         888  888      "88b  88K       88K       d8P  Y8b  88K               #
  ###          888    888  888  888  .d888888  "Y8888b.  "Y8888b.  88888888  "Y8888b.         ###  
 #####         Y88b  d88P  888  888  888  888       X88       X88  Y8b.           X88        ##### 
#######         "Y8888P"   888  888  "Y888888   88888P'   88888P'   "Y8888    88888P'       #######


from .Filex import *
from .Tuple_tools import *
from .RX_obj import *
from .System import *
#from .Date_Time import *

class rand:
    '''
    Random Variable Generator Class.
    '''
    @staticmethod
    def choose(iterator,k: int =1,duplicate=True):
        '''
        Return a random element from a non-empty sequence.
        '''
        if type(k)!=int: raise TypeError('k must be integer.')
        pass
        if k==1:
            return random.choice(iterator)
        elif k>1:
            if duplicate:
                return random.choices(iterator,k=k)
            else:
                return random.sample(iterator,k=k)
        else:
            raise ValueError('k Must Be Higher 0')
        
    @staticmethod
    def integer(first_number,last_number):
        '''
        Return random integer in range [a, b], including both end points.
        '''
        return random.randint(first_number,last_number)
    @staticmethod
    def O1(decimal_number=17):
        '''
        return x in the interval [0, 1)
        '''
        return round(random.random(),decimal_number)
    @staticmethod
    def number(first_number,last_number):
        '''
        return x in the interval [F, L]
        '''
        return random.uniform(first_number,last_number)


class style:
    '''
    This class is for Changing text Color,BG & Style.
    - style.print  to customize your print.
    - style.switch to change terminal colors.
    - style.switch_default for making everything default.
    '''
    def __init__(self,text,color='default',BG='black'):
        from colored import fg,bg,attr
        try: color= color.lower();BG=BG.lower()#;style=style.lower()
        except:pass        
        if color=='default':
            color=7 #188
        self.text= text     
        self.content= f"{fg(color)}{bg(BG)}{text}{attr(0)}"
    def __str__(self):
        return self.content
    def __repr__(self):
        return self.content
    def __add__(self,other):
        #print(type(other))
        if type(other)!=style:
            return self.content+other
        else:
            return self.content+other.content
    def __mul__(self,nom):
        return self.content*nom
    def __getitem__(self,index):
        return self.text[index]


    @staticmethod
    def print(text='',color='default',BG='default',style='None',end='\n'):
        '''
        text(text='Hello World',color='red',BG='white')
        output ==> 'Hello World' (With red color and white BG)
        Styles: bold - underline - reverse - hidden
         *bold and underline may not work. (Depends on terminal and OS)
        '''
        from colored import fg,bg,attr
        try: color= color.lower();BG=BG.lower();style=style.lower()
        except:pass
        if color=='default':
            color=7 #188
        if style=='none':
            style=0
        if color=='default' and BG!='default':
            print('%s%s%s%s' % (attr(style),bg(BG),text,attr(0)),end=end)
        if color!='default' and BG=='default':
            print('%s%s%s%s' % (attr(style),fg(color),text,attr(0)),end=end)
        if color=='default' and BG=='default':
            print('%s%s%s%s%s' % (attr(style),bg(BG),fg(color),text,attr(0)),end=end)

    @staticmethod
    def switch(color='default',BG='black',style='None'):
        '''
        Change color,BG and style untill you call it again and change them.
        '''
        try: color= color.lower();BG=BG.lower();style=style.lower()
        except:pass        
        if style=='none':
            style=0
        if color=='default':
            color=7
        from colored import fg,bg,attr
        print('%s%s%s' % (attr(style),bg(BG),fg(color)),end='')
    @staticmethod
    def switch_default():
        '''Switch Terminal Attributes to its defaults'''
        from colored import attr
        print('%s' % (attr(0)),end='')


class record:
    '''
    Use this method to record an action time in second.
    Usage:
        Start= record()
        #Some codes here...
        Finnish= Start.lap()
        print(Finnish) ==> 0.25486741
        #Some more codes here...
        Finnish= Start.lap() ==> 0.4502586
        Start.laps -->  [0.25486741, 0.4502586]
    Use Start.stop() to finnish recording and save memory.
    (after self.stop() using self.lap will cause error.)
    '''
    def __init__(self):
        self.__start= time.time()
        self.__end__=False
        self.laps=[]
    def __str__(self):
        if not self.__end__:
            running=True
        else:
            running=False
        return f'Running={str(running)} \nLaps: {self.laps}'
    def __repr__(self):
        if not self.__end__:
            running=True
        else:
            running=False
        return f'Running={str(running)} \nLaps: {self.laps}'

    class EndError(Exception):
        def __init__(self, message='Recording Has Been Finnished. Can Not Add a Lap.'):
            super().__init__(message)
    def lap(self,save=True):
        '''
        Return time passed from creating time of self.
        (Read 'record' Doc String)
        If save is True, time will be added to self.laps
        '''        
        if not self.__end__:
            lp= time.time()-self.__start
            if save:
                self.laps.append(lp)
            return lp
        else:
            raise self.EndError
    def stop(self):
        self.__end__=True
        '''del self
        return self.laps'''
    def reset(self,reset_start= False):
        '''
        This will erase self.laps 
        If reset_start is True, start time will reset too.
        '''
        self.laps= []
        if reset_start: self.__start= time.time()


#END
