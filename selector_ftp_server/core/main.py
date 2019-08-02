#Author:xyt
import os
import sys
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)

from core import selector_server_obj


def run():
    '''
    服务器端的入口程序。需要用户指定服务器的类型。（不能自动切换各种模式。）
    包括3种类型：
        1.回声服务器，对应的是SelEchoServer类。
        2.上传服务器，对应的是SelUploadServer类。
        3.下载服务器，对应的是SelDownloadServer类。

    :return:
    '''


    menu='''
1.echo server.
2.upload server.
3.download server.  
    '''

    while True:
        print(menu)
        choice=int(input("请输入你的选择：").strip())
        if choice==1:
            sel_obj=selector_server_obj.SelEchoServer()
            sel_obj.start()
        elif choice==2:
            sel_obj = selector_server_obj.SelUploadServer()
            sel_obj.start()
        elif choice==3:
            sel_obj=selector_server_obj.SelDownloadServer()
            sel_obj.start()
        else:
            print("NO such Item.")
            break