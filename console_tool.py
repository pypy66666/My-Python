﻿"""提供创建命令行程序工具的模块,包含Console类。
A module for creating command line programs."""
import sys,os,colorama,termcolor,time
import colorama.ansi as ansi

__email__="3416445406@qq.com"
__author__="七分诚意 qq:3076711200 邮箱:%s"%__email__
__version__="1.1.3"

BEL='\a' #振铃符
#color命令中的色彩代码
CMDCOLORS={"black":'0',"blue":'1',"green":'2',"aqua":'3',
           "red":'4',"purple":'5',"yellow":'6',"white":'7',
           "gray":'8',"light_blue":'9',"light_green":'A',
           "light_aqua":'B',"light_red":'C',"light_purple":'D',
           "light_yellow":'E',"bright_white":'F'}
RAINBOW=["red", "yellow", "green", "cyan", "blue","magenta","white"]

class ColoredTextWrapper():
    "在命令行提供带颜色的输出消息,类似于idle"
    def __init__(self,file=sys.stdout,color="white",bold=True):
        self.file=file
        self.color=color
        self.bold=bold
    def write(self,string):
        if self.file:
            print(termcolor.colored(string,color=self.color,
                                    attrs=(["bold" ] if self.bold else None)),
                  file=self.file,end="")
    def flush(self):pass


class Cursor(ansi.AnsiCursor):
    "命令行中的光标类"
    def __init__(self,outfile=sys.stdout):
        self.outfile=outfile
    def up(self,distance=1):
        "向上移动光标,距离为distance。"
        print(super().UP(distance),file=self.outfile,end='')
    def down(self,distance=1):
        "向下移动光标,距离为distance。"
        print(super().DOWN(distance),file=self.outfile,end='')
    def left(self,distance=1):
        "向左移动光标,距离为distance。"
        print(super().BACK(distance),file=self.outfile,end='')
    def right(self,distance=1):
        "向右移动光标,距离为distance。"
        print(super().FORWARD(distance),file=self.outfile,end='')
    def pos(self,x=1, y=1):
        """移动光标至指定位置(x,y)。
如果不提供参数x,y,则移动光标至屏幕左上角。"""
        print(super().POS(x,y),file=self.normalout,end='')


class Console():
    def __init__(self):
        colorama.init()
        #保留原来的sys.stdout和sys.stderr,以便调用colorize方法
        self.normalout,self.normalerr=sys.stdout,sys.stderr
        self.cur=Cursor(outfile=self.normalout) #初始化光标对象

    def bell(self,times=1,delay=False):
        """将振铃符发送至终端,发出响铃声。
times:响铃次数
delay:开始响铃后是否立即返回,默认为False。"""
        print(BEL*times,file=self.normalout)
        if delay: time.sleep(times*0.33)

    def color(self,backcolor='',forecolor=''):
        """改变命令行窗口的前景和背景颜色
与coloredtext方法不同,color改变整个窗口的颜色
该方法调用系统的color命令
如: color("blue","green") -- 设置前景颜色为绿色,背景颜色为蓝色
   color() -- 恢复默认颜色
可用的颜色: 可用的颜色: black, blue, green, aqua, red, purple, yellow, white, gray, light_blue, light_green, light_aqua, light_red, light_purple, light_yellow, bright_white"""
        cmd="color {}{}".format(CMDCOLORS.get[backcolor.lower()],
                               CMDCOLORS.get[forecolor.lower()])
        os.system(cmd)
    def coloredtext(self,string,color="white",
                    highlight=None,*args,end="\n",flush=False,reset=True):
        """输出一段带颜色的文本
        如:coloredtext("Hello world!",color="green",highlight="black","bold") --
        输出绿色、加粗的文字'Hello world!'"""
        if highlight and not highlight.startswith("on_"):
            highlight="on_"+highlight
        coloredtext=termcolor.colored(string,color=color,on_color=highlight,
                                      attrs=args)
        if not reset:
            coloredtext=coloredtext.replace(termcolor.RESET,"")
        print(coloredtext,end=end,file=self.normalout,flush=flush)
    def ctext(self,*args,**kwargs):
        "coloredtext函数的别名"
        self.coloredtext(*args,**kwargs)

    def colorize(self,stdout="blue",stderr="red",bold=True):
        """初始化带颜色的输出,类似于idle。
colorize(stdout="cyan",stderr="magenta") - 设置输出消息为青色,错误消息为紫色。
colorize(stderr=None) - 只设置输出消息(sys.stdout)的颜色。"""
        if stdout:
            sys.stdout=ColoredTextWrapper(self.normalout,color=stdout,bold=bold)
        if stderr:
            sys.stderr=ColoredTextWrapper(self.normalerr,color=stderr,bold=bold)
    def reset(self):
        "与colorize方法相反,停止带颜色的输出。"
        sys.stdout=self.normalout
        sys.stderr=self.normalerr
    def input(self,prompt='',chars_to_read=None,**kwargs):
        """获取用户的输入。
prompt:提示(默认显示为白色)
chars_to_read:要从sys.stdin读取多少个字符
"""
        self.ctext(prompt,end='',**kwargs)
        if chars_to_read:
            return sys.stdin.read(chars_to_read)[:-1]
        else:
            result=sys.stdin.readline()
            if not result:raise EOFError
            return result[:-1]

    def print_slowly(self,iterable_of_str,delay=0,*args,**kwargs):
        """缓慢地打印出一段文本
iterable_of_str:待打印的内容(字符串或可迭代对象)"""
        for char in iterable_of_str:
            start=time.perf_counter()
            self.coloredtext(char,end='',reset=False,*args,**kwargs)
            costedtime=time.perf_counter()-start
            if costedtime<delay:time.sleep(delay-costedtime)
        print(termcolor.RESET,end='')
    def title(self,title):
        "设置命令行窗口标题。"
        #os.system("title %s"%title)
        print(ansi.set_title(title),file=self.normalout,end='')
    def clear(self):
        "清除命令行窗口中的所有文本,这将调用系统的cls或clear命令。"
        os.system("cls" if sys.platform=='win32' else 'clear')

def test():
    c=Console()
    c.colorize()
    c.title("console_tool.py (Test)")
    c.coloredtext("Hello ","green","magenta","blink",reset=False,end="")
    print("world!",end="")
    sys.stderr.write(" \x01 \n") #\x01:笑脸符号

    story="""Once upon a time,there was a python module named console_tool,
wrote by {}.""".format(__author__)
    c.print_slowly(story,0.08,"yellow")
    c.input()
    c.cur.up(3)
    c.bell(1,delay=True)
    c.reset()

if __name__=="__main__":test()