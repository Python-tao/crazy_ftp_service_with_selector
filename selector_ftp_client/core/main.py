import os
import sys,threading
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
sys.path.append(BASE_DIR)


from core import sel_ftp_client
from conf import settings

'''
主函数，生成了SelClient类的实例ftp，运行了实例ftp的交互函数interactive()。

'''

def run():

    ftp = sel_ftp_client.SelClient()
    ftp.interactive()

