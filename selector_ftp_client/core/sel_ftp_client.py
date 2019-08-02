
import threading,socket
import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings
from core import server_file_reader
from core import muilt_socket_client


'''
与sel服务器端对应的客户端,使用threading实现并发上传和下载文件的功能。
为了与threading搭配使用，把socket用另外一个类muilt_socket_client实现。


'''

user_data = {
    'account_id':None,
    'is_authenticated':True,
    'current_dir':None,
    'account_data':None
}




class SelClient(object):
    '''
    SelClient类型，主要作用：
    1.处理客户端的交互界面。
    2.设定客户端的各种命令。包括以下：
        interactive，与用户进行交互，
        help，命令帮助菜单。
        echo，发送回音命令给服务端。
        get，下载文件。
        put，上传文件。

    构建函数中的变量：
        server_ip,服务器端的ip。
        server_port，服务器端的端口。
        messages，回声命令发送的内容。


    '''
    def __init__(self):
        self.server_ip=settings.selector_client_conf['server_host']
        self.server_port=settings.selector_client_conf['server_port']
        self.messages=settings.selector_client_conf['messages']
        # self.down_file_path=settings.para_conf['down_file_path']
    def help(self):
        '''
        打印帮助文档的函数。
        '''
        msg = '''
使用方法：
echo -thread 10 
put -thread 10 -local test.py
get -thread 1 -remote test.py

bye
        '''
        print(msg)

    def cmd_echo(self,*args):
        '''
        回音命令，
        向服务器发送回音信息，并打印出返回的信息。
        输入参数：
            thread_num，线程数，指明以多少个线程运行该命令。

        :param args:
        :return:
        '''
        cmd_split = args[0].split()
        if '-thread' in cmd_split:
            thread_num=cmd_split[cmd_split.index('-thread')+1]
            t_objs = []#用于保存创建的多个线程的内存地址。
            for i in range(int(thread_num)):
                s = muilt_socket_client.MuiltSocketClient(self.server_ip, self.server_port, self.messages)
                t1=threading.Thread(target= s.run_echo,)
                t1.start()
                t_objs.append(t1)
            for t in t_objs:
                t.join()#确保每个子线程都运行完。
            print("I am echoing.")
        else:
            self.help()











    def cmd_get(self,*args):
        '''
        此函数，用于并发下载文件。
        传入参数:
            filename,需要下载的远程服务器的文件名。
            thread_num，以多少个线程运行下载命令。

        '''
        cmd_split = args[0].split()
        if '-thread' and '-remote' in cmd_split:
            filename = cmd_split[cmd_split.index('-remote') + 1]
            thread_num = cmd_split[cmd_split.index('-thread') + 1]
            t_objs = []#用于保存创建的多个线程的内存地址。
            for i in range(int(thread_num)):
                s = muilt_socket_client.MuiltSocketClient(self.server_ip, self.server_port, self.messages)
                t1 = threading.Thread(target=s.run_get, args=(filename,))
                t1.start()
                t_objs.append(t1)
            for t in t_objs:
                t.join()#确保每个子线程都运行完。


        else:
            self.help()


    def cmd_put(self, *args):
        '''
         此函数的作用：
         并发上传多个文件。
         传入参数:
            filename,需要上传到服务器的本地的文件名。
            thread_num，开启多少个线程进行并发上传。

        '''
        cmd_split = args[0].split()
        if '-thread' and '-local' in cmd_split:
            filename=cmd_split[cmd_split.index('-local') + 1]
            abs_filename=settings.selector_client_conf['down_file_path']+'/'+filename
            thread_num = cmd_split[cmd_split.index('-thread') + 1]
            t_objs = []#用于保存创建的多个线程的内存地址。
            for i in range(int(thread_num)):
                s = muilt_socket_client.MuiltSocketClient(self.server_ip, self.server_port, self.messages)
                t1 = threading.Thread(target=s.run_put,args=(abs_filename,) )
                t1.start()
                t_objs.append(t1)
            for t in t_objs:
                t.join()#确保每个子线程都运行完。


        else:
            self.help()





    def interactive(self):
        '''
        交互函数
        获取用户输入的命令字符串。
        通过反射获取对应的实例方法。
        然后运行该方法。把命令字符串交给该实例方法。

        '''
        print("你好，欢迎进入Crazy Seletcors service sys，请输入你的命令。。")
        while user_data['is_authenticated'] is True:
            cmd = input(">>").strip()
            if len(cmd) ==0:continue
            cmd_str = cmd.split()[0]
            if hasattr(self,"cmd_%s" % cmd_str):
                func = getattr(self,"cmd_%s" % cmd_str)
                func(cmd)
            else:
                self.help()











