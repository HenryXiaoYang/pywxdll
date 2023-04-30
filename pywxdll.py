import json
from threading import Thread
from time import time

import websocket


class Pywxdll:
    def __init__(self, ip='127.0.0.1', port=5555):  # 微信hook服务器的ip地址和端口 The ip and port for wechat hook server
        self.ws_url = f'ws://{ip}:{port}'  # websocket url
        self.msg_list = []
        self.HEART_BEAT = 5005
        self.RECV_TXT_MSG = 1
        self.RECV_PIC_MSG = 3
        self.USER_LIST = 500
        self.GET_USER_LIST_SUCCSESS = 5001
        self.GET_USER_LIST_FAIL = 5002
        self.TXT_MSG = 555
        self.PIC_MSG = 500
        self.AT_MSG = 550
        self.CHATROOM_MEMBER = 5010
        self.CHATROOM_MEMBER_NICK = 5020
        self.PERSONAL_INFO = 6500
        self.DEBUG_SWITCH = 6000
        self.PERSONAL_DETAIL = 655
        self.DESTROY_ALL = 9999
        self.NEW_FRIEND_REQUEST = 37
        self.AGREE_TO_FRIEND_REQUEST = 10000
        self.ATTATCH_FILE = 5003

    def thread_start(self):  # 监听hook The thread for listeing
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.run_forever()

    def start(self):  # 开始监听 Start listening for incoming message
        wx = Pywxdll('127.0.0.1', port=5555)
        thread = Thread(target=wx.thread_start)
        thread.start()

    def on_open(self, ws):  # For websocket
        print('self', self)
        print('msglist', self.msg_list)
        print(f'{self.ws_url} opened successfully.')

    def on_message(self, ws, message):  # For websocket
        print(message)
        self.msg_list += message

    def on_error(self, ws, error):  # For websocket
        print(error)

    def on_close(self, ws, n1, n2):  # For websocket
        print(f'{self.ws_url} closed')

    ######## Recieve ########

    # 返回所有收到的信息 不建议使用 Return all the messages recieved  #USE IN CAUTION!
    def get_all_messages(self):
        return self.msg_list

    # 返回一部分收到的信息 建议使用 参数num用于设置返回的数量 Return lastest messages, to prevent the msg_list being too long   Arg num is for set the number of returning message
    def get_latest_messages(self, num):
        return self.msg_list[:num]

    # todo
    #  add function for returning only groupchat message / only personalchat message / message for specific group or person

    ######## Send ########

    # 发送txt消息到个人或群 wxid为用户id或群id content为发送内容  Send txt message to a wxid(perosnal or group)
    def send_txt_msg(self, wxid, content: str):
        qs = {
            'id': self.getid(),
            'type': self.TXT_MSG,
            'wxid': wxid,
            'roomid': 'null',
            'content': content,
            'nickname': "null",
            'ext': 'null'
        }
        s = json.dumps(qs)
        return s

    # 发送图片信息 wxid为用户id或群id path为发送图片的路径（建议用绝对路径） Send picture to wxid(perosnal or group)
    def send_pic_msg(self, wxid, path: str):
        qs = {
            'id': self.getid(),
            'type': self.PIC_MSG,
            'wxid': wxid,
            'roomid': 'null',
            'content': path,
            'nickname': "null",
            'ext': 'null'
        }
        s = json.dumps(qs)
        return s

    # 发送@信息 roomid为群id wxid为用户id nickname为@的人昵称 content为发送内容 send @ message
    def send_at_msg(self, roomid, wxid, nickname: str, content: str):
        qs = {
            'id': self.getid(),
            'type': self.AT_MSG,
            'roomid': roomid,
            'wxid': wxid,
            'content': content,
            'nickname': nickname,
            'ext': 'null'
        }
        s = json.dumps(qs)
        return s

    # 发送文件 wxid为用户id或者群id path为文件的路径 send attachment to chat or group
    def send_attach_msg(self, wxid, path):
        qs = {
            'id': self.getid(),
            'type': self.ATTATCH_FILE,
            'wxid': wxid,
            'roomid': 'null',
            'content': path,
            'nickname': "null",
            'ext': 'null'
        }

        s = json.dumps(qs)
        return s

    ######## 获取信息 ########

    # 获取唯一id
    def getid(self):
        return time() * 1000

    def heartbeat(h):
        return h

    # 获取账号信息 wxid为用户id get other user's information
    def get_personal_detail(self, wxid):
        qs = {
            'id': self.getid(),
            'type': self.PERSONAL_DETAIL,
            'content': 'op:personal detail',
            'wxid': wxid,
        }
        s = json.dumps(qs)
        return s

    # 获取登陆的账号信息 和get_personal_detail不同于get_personal_detail是获取其他用户的 get self's imformation
    def get_personal_info(self):
        qs = {
            'id': self.getid(),
            'type': self.PERSONAL_INFO,
            'content': 'op:personal info',
            'wxid': 'ROOT',
        }
        s = json.dumps(qs)
        return s

    # 获取微信通讯录用户名字和wxid get wechat address list username and wxid
    def get_contact_list(self):
        qs = {
            'id': self.getid(),
            'type': self.USER_LIST,
            'roomid': 'null',
            'wxid': 'null',
            'content': 'null',
            'nickname': 'null',
            'ext': 'null'
        }
        s = json.dumps(qs)
        return s

    # 获取群聊中用户昵称 wxid为群中要获取的用户id roomid为群id  get group's user's nickname
    def get_chat_nick(self, wxid, roomid):
        qs = {
            'id': self.getid(),
            'type': self.CHATROOM_MEMBER_NICK,
            'wxid': wxid,
            'roomid': roomid,
            'content': 'null',
            'nickname': 'null',
            'ext': 'null'
        }
        s = json.dumps(qs)
        return s

    # 获取群聊中用户列表 wxid为群id
    def get_chatroom_memberlist(self, wxid):
        qs = {
            'id': self.getid(),
            'type': self.CHATROOM_MEMBER,
            'roomid': 'null',
            'wxid': wxid,
            'content': 'null',
            'nickname': 'null',
            'ext': 'null'
        }
        s = json.dumps(qs)
        return s

    ######## 其他 ########
    def destroy_all(self):
        qs = {
            'id': self.getid(),
            'type': self.DESTROY_ALL,
            'content': 'none',
            'wxid': 'node',
        }
        s = json.dumps(qs)
        return s

##