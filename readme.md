# 主题：crazy_ftp_service_with_selector

需求：
    包括客户端和服务器端2个子程序。
    使用selectors封装了ftp服务器端程序，支持同时向多台客户端主机提供服务。
    支持并发文件上传和下载功能。
    服务器端使用epoll的方式响应客户端的请求。
    客户端主机使用threading多线程的方式向服务器发送并发请求。

