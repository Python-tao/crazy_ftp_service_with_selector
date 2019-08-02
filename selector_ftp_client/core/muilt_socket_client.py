#Author:xyt

import threading,socket
import os
import json
import hashlib
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings


class MuiltSocketClient(object):
    '''
    MuiltSocketClient类，用于所有socket相关的操作。
    主要的结构：
        __init__构建函数，用于创建socket实例，以及连接服务器端。
        send_interactive_msg，已废弃。
        run_echo，回音命令的具体执行。
        run_put，上传命令的具体操作。
        run_get，下载文件的具体操作。在Linux端下载会出错。待完善。


    '''
    def __init__(self,server_ip,server_port,messages):
        self.messages=messages
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server_ip,server_port))

    def send_interactive_msg(self,msg):
        self.sock.send(msg)
        print("send", msg)
        data=self.sock.recv(1024)
        if data:
            return True



    def run_echo(self):
        '''
        用于向服务器端发送回声消息。
        self.sock.send(message)，用于发送报文。
        db = self.sock.recv(1024)，用于接收报文。
        :return:
        '''
        for message in self.messages:
            print('%s: sending "%s"' % (self.sock.getsockname(), message))
            self.sock.send(message)
            data = self.sock.recv(1024)
            print('%s: received "%s"' % (self.sock.getsockname(), data))
            if not data:
                print('{}已经关闭 socket'.format(self.sock.getsockname()))
    def run_put(self,abs_filename):
        '''
        上传文件的具体操作。
        self.sock.send(line)，发送文件到服务器端。


        :param abs_filename: 本地文件的绝对路径。
        :return:
        '''
        if os.path.isfile(abs_filename):
            filesize = os.stat(abs_filename).st_size
            f = open(abs_filename, "rb")
            m = hashlib.md5()#实例化md5值对象。
            for line in f:
                m.update(line)#更新md5值。
                self.sock.send(line)
            else:
                print("文件上传成功...")
                print("file md5", m.hexdigest())
                f.close()


        else:
            print(abs_filename.split('/')[-1], "is not exist")



    def run_get(self,filename):
        '''
        下载文件的具体操作。
            1.首先发送一个字典给服务器端，主要是文件名，目的是告诉服务器需要下载什么文件。
            2.db=self.sock.recv(1024)，接收服务器发送过来的文件大小的信息。此信息用于判断后续接收报文的大小。
            3.


        :param filename: 待下载的文件名
        abs_filename:下载到本地时使用的文件绝对路径。
        :return:
        '''
        local_port = self.sock.getsockname()[1]
        abs_filename = settings.selector_client_conf['down_file_path'] + '/' + filename + '.' + str(local_port)
        if not os.path.isfile(abs_filename):
            msg={
                'action':'get',
                'filename':filename,
            }
            print('%s: sending "%s"' % (self.sock.getsockname(), msg))
            self.sock.send(json.dumps(msg).encode())
            data=self.sock.recv(1024)
            res_dic=json.loads(data.decode())
            file_total_size=res_dic['res_data']
            received_size = 0
            print('文件大小为：',file_total_size)
            f = open(abs_filename, "wb")
            while received_size < file_total_size:
                if file_total_size - received_size > 1024:
                    size = 1024
                else:
                    size = file_total_size - received_size
                data = self.sock.recv(size)
                received_size += len(data)
                f.write(data)
            else:
                print('文件接收完毕。')
                f.close()
                f2=open(abs_filename,'rb')#计算md5值，确保文件大小无误。
                m=hashlib.md5()
                m.update(f2.read())
                print("md5:",m.hexdigest())
                f2.close()


        else:
            print("本地已经存在同名的文件。")
