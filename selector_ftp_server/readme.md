# 主题：selector_ftp_server

需求：
    ftp服务端程序，提供三者工作模式，支持响应客户端发送回声命令，并发文件上传和下载功能。
    主要是测试selector的并发响应能力。

#工作模式
## echo server模式已完成)
```
　　作用：接收客户端发送回声请求，服务器接收然后回显。

```


## upload server模式(已完成)
```
    作用:
        接收客户端发送过来的文件。
        支持客户端并发发送文件过来。
        在Linux环境下，服务端可以逐一响应并处理大量请求而不会崩溃，充分证明了系统的稳定性。      
```

## download server模式(待完善)
```
    作用:
        响应客户端的请求，把文件发送给客户端。
        在window下，可以正常工作。
        在linux端，下载的文件超过一定大小就会报错。
    
```




# 使用的模块
```
    socket，  创建socket套接字。
    selectors，    select多路复用模型的实现。
    
```



# 目录结构
```
- bin 
    -run_server.py          程序启动入口
- conf
    -settinggs.py           全局配置文件，保存了本地下载路径,ftp服务器的ip和端口。   
-core                        核心代码
    -main.py                主函数.
    -selector_server_obj.py ftp服务器的各个功能模块。
-data                           本地下载文件目录
readme.md                       readme文件
```