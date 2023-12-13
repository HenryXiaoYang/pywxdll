# <u>**pywxdll**</u>

一个用于基于hook的微信机器人的Python库

## <u>安装pywxdll</u>

在终端中输入 `pip install pywxdll` 即可


***

## <u>配制环境</u>

### 方法1: Docker

使用Docker可在x86的 Windows Linux MacOS 上运行

请在这个docker环境下运行：https://github.com/ChisBread/wechat-service/

这个docker只支持x86芯片，arm芯片无法运行 (苹果m系列的别想了(~~不嫌烦有解决方法，自行搜索utm~~))

#### 1. 安装Docker

装好了可跳过

如何安装这里就不说了，自己搜下

官方教程链接🔗：

https://docs.docker.com/get-docker/

#### 2. 拉取Docker镜像

```bash
#拉取镜像
docker pull chisbread/wechat-service
```

#### 3. 运行Docker

```bash
#启动Docker
docker run --name wechat-service \
    -e HOOK_PROC_NAME=WeChat \
    -e HOOK_DLL=auto.dll \
    -e TARGET_AUTO_RESTART="yes" \
    -e INJ_CONDITION="[ \"\`sudo netstat -tunlp | grep 5555\`\" != '' ] && exit 0 ; sleep 5 ; curl 'http://127.0.0.1:8680/hi' 2>/dev/null | grep -P 'code.:0'" \
    -e TARGET_CMD=wechat-start \
    -p 4000:8080 -p 5555:5555 -p 5900:5900 \
    --add-host=dldir1.qq.com:127.0.0.1 \
    chisbread/wechat-service
```

#### 4. 登陆微信

在登陆微信账号前，用于hook的dll注入也没用，所以登陆后才会注入。

使用浏览器访问`http://<服务器IP(本地部署是127.0.0.1)>:4000/vnc.html`

点击`連線`连接到vnc

连接后浏览器中会有微信登陆页面，用手机扫码登陆即可。

### 方法2: Windows微信注入

此方法仅支持 x68 Windows

## 环境准备完毕

微信登陆后环境准备完毕


***

# 简单小例子

```python
import pywxdll

# 注意需要在docker环境内运行
bot = pywxdll.Pywxdll('127.0.0.1', 5555)  # 获得Pywxdll实例
bot.start()  # 开始监听微信信息
print(bot.get_contact_list())  # 获取微信通讯录列表并打印

while True:
    if bot.msg_list:  # 如果机器人消息列表中有东西
        msg = bot.msg_list.pop(0)  # 获取消息列表第一项并pop
        if msg['content'] == 'hi':  # 如果消息内容为hi
            bot.send_txt_msg(recv['wxid'], 'hello')  # 向发送hi的人发送hello
```

***

# 如何使用pywxdll

## 写在前面

`wxid`与`wxcode`是有区别的

`wxid`: 微信内部使用的用户id。以前与wxcode相同，能修改。现在改不了了。所以新用户的wxid以`wxid_`开头，老用户的会是他们修改过的。

`wxcode`: 你加微信时用的微信号，用户能在微信设置中修改

## 获得Pywxdll实例

```python
pywxdll.Pywxdll(self, ip: str, port: int)
```

ip: 部署的docker的ip，如果为本地部署则为127.0.0.1，不填写则默认为127.0.0.1

port: 部署的docker的api端口，可在启动docker时修改（上文启动docker是写的5555），不填写则默认为5555

例子：

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)  # 获得Pywxdll实例
```

## 开始监听微信消息

监听微信消息，不调用一下的话无法收到消息哦

```python
start(self)
```

无参数

例子：

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()  # 开始监听微信信息
```

## 获取收到的信息

当收到一个消息时，Pywxdll实例的属性：`msg_list`列表中会被加入一个字典。这个字典中存放了收到的消息，以及其他有用的信息。

具体如下：

```
群聊消息：
{'content': '收到的信息', 'id': '20231026225736 这条消息的id', 'id1': 'wxid_12345678900000 发送人的wxid', 'id2': '', 'id3': '', 'srvid': 1, 'time': '2023-10-26 11:45:14', 'type': 1, 'wxid': '12345678900@chatroom 群的群id'}

朋友消息：
{'content': '收到的信息', 'id': '20231026225736 这条消息的id', 'id1': '', 'id2': '', 'id3': '', 'srvid': 1, 'time': '2023-10-26 11:45:14', 'type': 1, 'wxid': 'wxid_12345678900000 发送人的wxid'}
```

例子：

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

while True:
    if bot.msg_list:  # 如果信息列表中有信息
        print(bot.msg_list.pop(0))  # pop并打印
```

## 发送文本消息

```python
send_txt_msg(self, wxid: str, content: str)
```

wxid: 微信号(新用户的wxid以wxid_开头 老用户他们可能修改过 现在改不了)或者群号(以@chatroom结尾)

content: 要发送的文本

返回值: 字典

```python
# 发送成功时返回这个
{'content': 'send txt msg:asm execution succsessed', 'id': '20231027003009', 'receiver': 'CLIENT', 'sender': 'SERVER',
 'srvid': 1, 'status': 'SUCCSESSED', 'time': '2023-10-27 11:45:14', 'type': 555}
```

例子：

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

bot.send_txt_msg('12345678900@chatroom', 'hello,world!')  # 把hello,world!发送到群12345678900@chatroom
bot.send_txt_msg('wxid_12345678900000', 'hello,world!')  # 把hello,world!发送到朋友wxid_12345678900000
```

## 发送图片消息

```python
send_pic_msg(self, wxid: str, path: str)
```

wxid: 微信号(新用户的wxid以wxid_开头 老用户他们可能修改过 现在改不了)或者群号(以@chatroom结尾)

path: 图片路径。请特别注意下这个，这里是docker中的路径！！！

例子:

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

# 注意图片路径是docker中的路径，不是本地路径
bot.send_pic_msg('12345678900@chatroom',
                 '/pictures/picture.png')  # 把路径为 /pictures/picture.png 的图片发到了发送到群12345678900@chatroom
bot.send_pic_msg('wxid_12345678900000',
                 '/pictures/picture.png')  # 把路径为 /pictures/picture.png 的图片发送到朋友wxid_12345678900000
```

## 发送@消息

```python
send_at_msg(self, roomid: str, wxid: str, nickname: str, content: str)
```

roomid: 群号(以@chatroom结尾)

wxid: 要@的人的wxid(新用户的wxid以wxid_开头 老用户他们可能修改过 现在改不了)

nickname: 要@的人的昵称，可随意修改

content: 要发送的文本

例子:

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

bot.send_at_msg('12345678900@chatroom', 'wxid_12345678900000', 'HenryXiaoYang',
                'Hello!')  # 在群12345678900@chatroom中，使用HenryXiaoYang这个昵称@了wxid为wxid_12345678900000的用户，并发送了Hello!
```

## 发送文件消息

```python
send_attach_msg(self, wxid: str, path: str)
```

wxid: wxid(新用户的wxid以wxid_开头 老用户他们可能修改过 现在改不了)或者群号(以@chatroom结尾)

path: 文件的路径。请特别注意下这个，这里是docker中的路径！！！

例子:

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

# 注意文件路径是docker中的路径，不是本地路径
bot.send_pic_msg('12345678900@chatroom',
                 '/files/lotofthings.zip')  # 把路径为 /files/lotofthings.zip 的文件发到发送到群12345678900@chatroom
bot.send_pic_msg('wxid_12345678900000',
                 '/files/lotofthings.zip')  # 把路径为 /files/lotofthings.zip 的文件发送到朋友wxid_12345678900000
```

## 获取其他微信账号信息

似乎有问题，给我点时间调试。

```python
get_personal_detail(self, wxid: str)
```

wxid: wxid(新用户的wxid以wxid_开头 老用户他们可能修改过 现在改不了)

返回值: Dictionary

```python
{'big_headimg': '大头像图片链接', 'cover': '貌似是封面？这个我没看过有', 'little_headimg': '小头像图片链接',
 'signature': '个人签名'}
```

例子:

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

print(bot.get_personal_detail(
    wxid_12345678900000))  # {'big_headimg': 'http://linktobig_headimg', 'cover': 'http://linktocover', 'little_headimg': 'http://linktolittle_headimg', 'signature': '个人签名'}
```

## 获取微信通讯录

获取微信通讯录用户名字和wxid

```python
get_contact_list(self)
```

无参数

返回值: list

```python
[
    {'headimg': 'https://linktoheadimg', 'name': '我是群名', 'node': 000000001, 'remarks': '',
     'wxcode': '00000000001@chatroom', 'wxid': '12345678901@chatroom'},
    {'headimg': 'https://linktoheadimg', 'name': '我是朋友名1', 'node': 000000002, 'remarks': '',
     'wxcode': 'friendswxcode1', 'wxid': 'wxid_00000000000001'},
    {'headimg': 'https://linktoheadimg', 'name': '我是朋友名2', 'node': 000000003, 'remarks': '',
     'wxcode': 'friendswxcode2', 'wxid': 'wxid_00000000000002'},
    {'headimg': 'https://linktoheadimg', 'name': '我是朋友名3', 'node': 000000004, 'remarks': '',
     'wxcode': 'friendswxcode3', 'wxid': 'wxid_00000000000003'}
]
```

例子:

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

print(bot.get_contact_list())  # 获取微信通讯录用户名字和wxid
```

## 获取群聊中用户昵称

```python
get_chatroom_nickname(self, roomid: str, wxid: str)
```

参数：

roomid: 群号(以@chatroom结尾)

wxid: wxid(新用户的wxid以wxid_开头 老用户他们可能修改过 现在改不了)

返回值: Dictionary

```python
{'nick': '我是群昵称', 'roomid': '0000000001@chatroom', 'wxid': 'wxid_0000000000001'}
```

例子:

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

print(bot.get_chatroom_nickname('0000000001@chatroom',
                                'wxid_0000000000001'))  # 获取群聊0000000001@chatroom中用户wxid_0000000000001的昵称
```

## 获取朋友昵称

```python
get_user_nickname(self, wxid: str)
```

参数：

wxid: wxid(新用户的wxid以wxid_开头 老用户他们可能修改过 现在改不了)

返回值: Dictionary

```python
{'nick': '朋友昵称', 'roomid': 'null', 'wxid': 'wxid_00000000000001'}
```

例子:

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

print(bot.get_user_nickname('wxid_0000000000001'))  # 获取用户wxid_0000000000001的昵称
```

## 获取群聊中用户列表

```python
get_chatroom_memberlist(self, roomid: str)
```

参数：

roomid: 群号(以@chatroom结尾)

返回值:

```python
{'address': 000000001, 'member': ['wxid_0000000000001', 'wxid_0000000000002'], 'room_id': '0000000001@chatroom'}
```

例子:

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()

print(bot.get_chatroom_memberlist('0000000001@chatroom'))  # 获取群0000000001@chatroom的成员列表
```