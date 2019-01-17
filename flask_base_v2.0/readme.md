# API_Server（主节点）

This Server is used for sending domain's whois query to Client machine

### 说明：基于flask和gevent的whois任务分发的并发API

### 功能：根据用户发来的域名在数据库中找到对应的whois服务器，将域名和对应的whois服务器发送给API从节点，可以选择性的加上对应的代理信息一并发送个给子节点

#### 特性：
  1. 心跳感知：
      ##### 1.1 主从节点采用心跳的的方式进行感知，若从节点出现崩溃的情况，主节点则将其从effective节点中去除崩溃的节点，等待下一次心跳感知
      ##### 1.2 若从节点崩溃，主节点则会向管理员发送邮件，告知哪几个节点出现问题，管理员可以通过邮件内容找到出错的节点并进行维护
  2. 并发：
      ##### 2.1 基于```gevent monkek```和 ```gevent WSGIServer```的高性能并发模型，同时并发处理上限还没有做过压力测试
  3. proxy：
      ##### 3.1 proxy在发送时是可选的，不加proxy，API从节点也可进行whois探测，不过为了保证稳定，添加代理是一种必要的方法
      
#### 过程
  用户只需向API_Server发送域名即可，如
  ```http://localhost:port/WHOIS/baidu.com```
  API_Server会对baidu.com进行处理，并将其加上对应的whois服务器（可选择加上代理），发送给API从节点，从节点返回whois数据给API_Server，API_Server再将其返回给用户
  
#### 效率
   目前测试过10w域名的whois请求，采用4个API从节点进行探测，探测速度约```0.06s/个```，whois信息正确率```95%+```
   
#### Contact
wjx.wud@gmail.com
Harbin Institute of Technology
