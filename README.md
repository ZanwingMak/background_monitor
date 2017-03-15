# background_monitor

blog：https://gfwboom.com/archives/code/python/2015/11/13/37.html

后台监听操作[键盘、粘贴事件、自动截图]

您是否遇到过，借用电脑给朋友使用，但是却不放心他会不会偷看你的私人文件的情况？只要在后台启用了该程序，便会监听记录键盘的按键信息和粘贴复制事件，同时会保存日志到程序目录下的Monitor文件夹里，而且还会在窗口焦点改变时，自动全屏截图并保存到Monitor目录下的img文件夹里。现在，你可以在后台运行此程序，把电脑借给朋友，测试一下他吧！

其实下一步可以将功能进一步提升，例如自动发送邮件到指定邮箱、或者将信息传输到服务器等。

主要使用库：ctypes、pythoncom、pyHook、win32api、win32con、win32gui、win32ui、Image、PyQt4

【EXE打包】链接: http://pan.baidu.com/s/1sjQRZWx 密码: 5bkb

![image](https://gfwboom.b0.upaiyun.com/usr/uploads/2016/04/1736896966.jpg)
![image](https://gfwboom.b0.upaiyun.com/usr/uploads/2016/04/2530687481.jpg)
