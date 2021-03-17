## 简介 

mini-socket 提供了一个简易版本的多连接socket. 

## 连接

### Basic 

简单的连接方式是: 

Machine A: 挂服务端;  Machine B: 挂客户端. A/B 属于同局域网.

B 发数据 -> A 收并记录, 告知B已收到 -> 连接关闭

B 请求数据 -> A 收到请求, 查找并发数据 -> B 收到数据, 并告知A已收到 -> 连接关闭

以上完成两个机器之间简单收发. Machine B可以是不同ip机器(复数). 

### Mid

在一些情况下, 如由于安全问题, 可能没办法暴露相关端口,  导致 A/B 无法连接. 

建立一个中间连接, Machine C, 用于连接A B . 

中转连接方式: 

Machine C: 挂服务端; Machine A/B: 挂客户端. 

收发数据和 basic 相同.  同样的,  A 和 B也可以是不同ip 机器 (复数). 

一些项目使用的情况不同, 需要解析收发数据的形式. 

`server.MidServer` 是为项目定制的解析方式, 需要别的在`server.py` 里面加就好. 

## Usage

挂服务端: 

`python echo_server.py ${IP}$ ${PORT}$`

`IP`: 局域网下ip or localhost 都可以

客户端:

`python echo_client.py ${IP}$ ${PORT}$ ${TYPE}$ ${CONTENT}$ `

`TYPE`:  请求数据 用 `search` ; 发数据 非 `search`  的任何字符都可以. 


## TODO

- [ ] add quiet mode