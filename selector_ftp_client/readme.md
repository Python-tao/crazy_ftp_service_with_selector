# 主题：selector_ftp_client

需求：
    ftp客户端程序，提供命令行界面，支持向服务器并发发送回声命令，并发文件上传和下载功能。
    主要是测试selector的并发响应能力。

#命令行格式
## echo命令(已完成)
```
　　作用：向远程服务器发送回声命令，服务器接收然后回显。
   格式：
        echo -thread [Thread_Numbers]
            -thread [Thread_Numbers],指明启动多少个线程向后端服务器发送命令。
            
   示例：
        echo -thread 10

```


## put命令(已完成)
```
    作用:
        上传文件到远程服务器。
    格式：
        put -thread [Thread_Numbers] -local [local_file_name]
            -thread [Thread_Numbers],指明启动多少个线程向后端服务器上传文件。
            -local [local_file_name]，指明需要上传的文件名，该文件需要放在本地的data目录下。

    示例：
        put -thread 10 -local test.py         
```

## get命令(已完成)
```
    作用:
        上传文件到远程服务器。
    格式：
        put -thread [Thread_Numbers] -remote [remote_file_name]
            -thread [Thread_Numbers],指明启动多少个线程向后端服务器下载文件。
            -remote [remote_file_name]，指明需要下载的文件名。

    示例：
        get -thread 1 -remote test.py         
```




# 使用的模块
```
    socket，  创建socket套接字。
    threading       多线程模块
    
```



# 目录结构
```
- bin 
    -run_client.py          程序启动入口
- conf
    -settinggs.py           全局配置文件，保存了本地下载路径,ftp服务器的ip和端口。   
-core                        核心代码
    -main.py                主函数.
    -muilt_socket_client.py 创建socket与服务器连接的模块。
    -sel_ftp_client.py      ftp客户主要交互的函数。
-data                           本地下载文件目录
readme.md                       readme文件
```