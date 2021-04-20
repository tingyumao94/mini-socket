## 简介 

mini-socket 提供了一个简易版本的多连接socket. 

## 连接

### Basic 

简单的连接方式是: 

Machine A: 挂服务端;  Machine B: 挂客户端. A/B 属于同局域网.

B 发数据 -> A 收并记录, 告知B已收到 -> 连接关闭

B 请求数据 -> A 收到请求, 查找并发数据 -> B 收到数据, 并告知A已收到 -> 连接关闭


### Mid

在一些情况下, 如由于安全问题, 可能没办法暴露相关端口,  导致 A/B 无法连接. 

建立一个中间连接, Machine C, 用于连接A B . 

中转连接方式: 

Machine C: 挂服务端; Machine A/B: 挂客户端. 

收发数据和 basic 相同. 

一些项目使用的情况不同, 需要解析收发数据的形式. 

`server.MidServer` 是为该方法的数据解析方式, 需要别解析方式在`server.py` 里面加. 

## Usage

挂服务端: 

`python echo_server.py ${IP}$ ${PORT}$`

`IP`: 局域网下ip or localhost 都可以

客户端:

`python echo_client.py ${IP}$ ${PORT}$ ${TYPE}$ ${CONTENT}$ `

`TYPE`:  请求数据 用 `search` ; 发数据 非 `search`  的任何字符都可以. 

## 跨机延时测试

例子:  以basic 的方式为例. 

machine A: 挂server,用于测延时

```
# global vars
HOST = "10.130.19.34" 
PORT = 7788
```

`python echo_server.py $HOST $PORT.`

A B 能正常通信的情况下:

Machine B: 挂client, 用于跑search代码.

先不管search, 先说一下相关的数据处理. 

`python echo_client.py $HOST $PORT net '32_32_32_128_3_3_3_3'`


B向A发了网络的结构数据, A中需要测改网络的延时, 在demo中返回了一个随机数, 实际中需要手动改一下相关代码. 

A完成了延时测试, B可以query 延时结果.  

`python echo_client.py $HOST $PORT search '32_32_32_128_3_3_3_3'`

以上完成了一次网络延时测试. 

在search 中, 基本逻辑也是这样的. 

不同的地方在于: 在发送网络后, B不知道A何时完成测试, 会一直query, 如果A没有完成, 返回的字符会带"NO", 以此作为是否A是否完成的flag .

```python
from minisocket.client import Client 
# sending
for i, net in enumerate(net_list):
    assert isinstance(net, dict)
    str_net = dict2str(net)
    clinet = Client(host, port, 'net', str_net)
    client.run()
    # send -> query(waiting) 
    while True:
        client = Client(host, port, 'search', str_net)
        client.run()
        if "No" not in client.recv_info:
            # finished flag
            lat = client.recv_info
            net["tlats"] = float(lat)
            break
```
   
## TODO

- [ ] add quiet mode