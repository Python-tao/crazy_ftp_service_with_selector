import os
import time
import hashlib
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)

import selectors
import socket
import hashlib
import json
from conf import settings


class SelEchoServer(object):
    '''
    回音服务器的类。使用了selectors是为了同时响应客户端的并发访问请求。
    各方法的作用:
        __init__,构建函数，实例化selectors。
        echo（），对新连接运行echo方法。
        accept（），接入客户端新连接，创建客户端实例conn；把conn注册为selectors事件
        start（），入口函数，创建服务端的socket，把socket注册为selectors事件
            阻塞并遍历events中的事件。一旦有事件出现，就执行该事件对应的回调函数。


    '''
    def __init__(self):
        self.sel = selectors.DefaultSelector()




    def echo(self,conn,mask,*args):
        '''
        echo函数，用于回音服务器的具体操作的函数。
        一旦客户端有报文接入，就接收报文，返回把报文转发给客户端。
        :param conn: 已接入的客户端请求socket的实例。
        :param mask: 作用不明。
        :param args: 其它参数。
        :return:
        '''
        data = conn.recv(1024)  # Should be ready
        if data:
            print('echoing,recv:', repr(data))
            conn.send(data)  # Hope it won't block

        else:
            # print('closing', conn)
            self.sel.unregister(conn)#一旦客户端断开连接，就取消注册。
            conn.close()#关闭连接。

    def accept(self,sock, mask):#创建客户的新连接
        conn, addr = sock.accept()  # 使用accept方法，实例化新客户端socket为conn。
        # print('accepted', conn, 'from', addr,mask)
        conn.setblocking(False)#设置为非阻塞。
        self.sel.register(conn, selectors.EVENT_READ, self.echo) #新连接注册interactive回调函数与客户端交互



    def start(self):
        '''
        入口函数。
            创建服务器端的socket，绑定在对应的ip和端口，监听。
            把socket注册为selectors监听的事件以及相应的回调函数accept。
            循环并阻塞在events列表的读取中。
            一旦有新事件，就运行事件对应的回调函数。
            key.fileobj，socket的实例。

        :return:
        '''
        sock = socket.socket()
        local_ip=settings.sel_ftp_config['server_host']
        local_port=settings.sel_ftp_config['server_port']

        sock.bind((local_ip, local_port))
        sock.listen(100)
        sock.setblocking(False)#设置为非阻塞。
        self.sel.register(sock, selectors.EVENT_READ, self.accept)
        print("Crazy Selector ECHO Server is Running")

        while True:
            events = self.sel.select()  # 默认阻塞，有活动连接就返回活动的连接列表
            for key, mask in events:
                callback = key.data  # accept
                callback(key.fileobj, mask)  # key.fileobj=  文件句柄




class SelUploadServer(object):
    #文件上传服务器模式。
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.filename = 'test.txt'

    def put(self,conn,mask,*args):
        '''
        接收客户端的发送过来的文件，并保存到本地。
        abs_filename，根据客户端的port，在本地创建对应的文件名。
        不断保存客户端发送过来的报文。并写入本地的文件中。

        :param conn: 客户端新请求的socket实例
        :param mask: 不明。
        :param args: 其它参数。
        :return:
        '''
        remote_port=repr(conn).split('raddr=')[-1].split(' ')[-1].strip(')>')
        abs_filename = settings.sel_ftp_config['root_file_path'] + '/' + self.filename+'.'+remote_port
        f = open(abs_filename, "ab")
        data = conn.recv(1024)  # Should be ready

        if data:
            f.write(data)

        else:
            print('文件接收完毕。')

            f.close()
            f2=open(abs_filename, "rb")
            m = hashlib.md5()
            m.update(f2.read())
            print("md5:", m.hexdigest())
            f2.close()
            print('closing', conn)
            self.sel.unregister(conn)
            conn.close()


    def accept(self,sock, mask):#创建客户的新连接
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr,mask)
        conn.setblocking(False)

        self.sel.register(conn, selectors.EVENT_READ, self.put) #新连接注册interactive回调函数与客户端交互



    def start(self):
        sock = socket.socket()
        local_ip=settings.sel_ftp_config['server_host']
        local_port=settings.sel_ftp_config['server_port']

        sock.bind((local_ip, local_port))
        sock.listen(100)
        sock.setblocking(False)
        self.sel.register(sock, selectors.EVENT_READ, self.accept)





        print("Crazy Selector Upload Server is Running")


        while True:
            events = self.sel.select()  # 默认阻塞，有活动连接就返回活动的连接列表
            for key, mask in events:
                callback = key.data  # accept
                callback(key.fileobj, mask)  # key.fileobj=  文件句柄


class SelDownloadServer(object):
    #文件下载服务器模式。
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.filename = 'test.txt'



    def get(self,conn,mask,*args):
        '''
        发送服务器端的文件给客户端。
        功能不完善。

        :param conn:
        :param mask:
        :param args:
        :return:
        '''
        data = conn.recv(1024)  # Should be ready
        if data:
            msg_dic=json.loads(data.decode())
            abs_filename = settings.sel_ftp_config['root_file_path'] + '/'+msg_dic['filename']
            if os.path.isfile(abs_filename):

                file_size = os.stat(abs_filename).st_size
                response_data = {'res_type': 0, 'res_data': file_size}
                conn.send(json.dumps(response_data).encode("utf-8"))


                m = hashlib.md5()
                f=open(abs_filename,'rb')


                for line in f:
                    # m.update(line)
                    conn.send(line)
                f.close()
                # print("file md5", m.hexdigest())
                print("文件发送完毕。")

            else:
                print("无此文件。")
                self.sel.unregister(conn)
                conn.close()


        else:
            print('closing', conn)
            self.sel.unregister(conn)
            conn.close()




    def accept(self,sock, mask):#创建客户的新连接
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr,mask)
        conn.setblocking(False)

        self.sel.register(conn, selectors.EVENT_READ, self.get) #新连接注册执行get回调函数与客户端交互



    def start(self):
        sock = socket.socket()
        local_ip=settings.sel_ftp_config['server_host']
        local_port=settings.sel_ftp_config['server_port']

        sock.bind((local_ip, local_port))
        sock.listen(100)
        sock.setblocking(False)
        self.sel.register(sock, selectors.EVENT_READ, self.accept)





        print("Crazy Selector Download Server is Running")


        while True:
            events = self.sel.select()  # 默认阻塞，有活动连接就返回活动的连接列表
            for key, mask in events:
                callback = key.data  # accept
                callback(key.fileobj, mask)  # key.fileobj=  文件句柄


