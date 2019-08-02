# __author__ = "XYT"

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

'''
全局配置文件
    down_file_path，本地的下载目录的绝对路径。
    

'''


selector_client_conf = {
    'engine': 'file_storage',  # support mysql,postgresql in the future
    'name': 'accounts',
    'down_file_path': "%s/data" % BASE_DIR,
    'host_file_path':"%s/conf/sample_host.ini" % BASE_DIR,
    'server_host': 'localhost', #ftp服务器的ip
    'server_port': 9999,         #ftp服务器的端口
    'messages':[ b'This is the message. ',  #
             b'It will be sent ',
             b'in parts.',
             ]

}

# messages = [ b'This is the message. ',
#              b'It will be sent ',
#              b'in parts.',
#              ]




