#coding:gbk

import socket
import threading
import time
import struct

#监听的ip及端口
bind_ip = '127.0.0.1'
bind_port = 12450

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((bind_ip,bind_port))
s.listen(0)
print u'等待连接...'

def tcplink(sock,addr):
    print u'[*] 正在监听 ip:%s 端口:%d' % (bind_ip,bind_port)
    FILEINFO_SIZE = struct.calcsize('128sI')
    '''定义文件信息（包含文件名和文件大小）大小。128s代表128个char[]（文件名），I代表一个integer or long（文件大小）'''
    while True:     
        try:
            fhead = sock.recv(FILEINFO_SIZE)
            filename, filesize = struct.unpack('128sI', fhead)
            '''把接收到的数据库进行解包，按照打包规则128sI'''
            print u"地址：",addr
            print filename, len(filename),type(filename)
            print filesize
            filename = 'new_' + filename.strip('\00')#命名文件接收到的文件
            fp = open(filename,'wb')#新建文件，并且准备写入
            restsize = filesize
            print u'正在接收...'
            while 1:
                if restsize > 10485600:#如果剩余数据包大于10m，就取10m的数据包
                    filedata = sock.recv()
                else:
                    filedata = sock.recv(restsize)
                    fp.write(filedata)
                    break
                if not filedata:
                    break
                fp.write(filedata)
                restsize = restsize - len(filedata)#计算剩余数据包大小
                if restsize <= 0:
                    break
            fp.close()
            print "接收成功!!文件名:",filename
        except:
            print "连接已断开..."
            sock.close()
            break
 

while True:
    sock,addr = s.accept()
    t = threading.Thread(target=tcplink,args=(sock,addr))
    t.start()

