import threading
import time

import requests
import websocket

from .pywxdll_json import *

HEART_BEAT = 5005
RECV_TXT_MSG = 1
RECV_PIC_MSG = 3
NEW_FRIEND_REQUEST = 37
RECV_TXT_CITE_MSG = 49
PIC_MSG = 500
AT_MSG = 550
TXT_MSG = 555
USER_LIST = 5000
GET_USER_LIST_SUCCSESS = 5001
GET_USER_LIST_FAIL = 5002
ATTATCH_FILE = 5003
CHATROOM_MEMBER = 5010
CHATROOM_MEMBER_NICK = 5020
DEBUG_SWITCH = 6000
PERSONAL_INFO = 6500
PERSONAL_DETAIL = 6550
DESTROY_ALL = 9999
JOIN_ROOM = 10000


class Pywxdll:
    def __init__(self, ip='127.0.0.1', port=5555):  # 微信hook服务器的ip地址和端口 The ip and port for wechat hook server
        self.ip = ip
        self.port = port
        self.ws_url = f'ws://{ip}:{port}'  # websocket url
        self.msg_list = []

    def thread_start(self):  # 监听hook The thread for listeing
        websocket.enableTrace(False)  # 开启调试？
        ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.run_forever()

    def start(self):  # 开始监听 Start listening for incoming message
        wxt = threading.Thread(target=self.thread_start)
        wxt.daemon = True
        wxt.start()

    def on_open(self, ws):  # For websocket
        pass

    def on_message(self, ws, message):  # For websocket
        recieve = json.loads(message)
        r_type = recieve['type']
        if r_type == 5005:
            pass
        elif r_type == 1 or r_type == 3:
            self.msg_list.append(self.recv_txt_handle(recieve))

    def on_error(self, ws, error):  # For websocket
        print(error)

    def on_close(self, ws):  # For websocket
        pass

    ######## Recieve ########

    # 返回所有收到的信息 不建议使用 Return all the messages recieved  #USE IN CAUTION!
    def get_all_messages(self):
        return self.msg_list

    # 返回一部分收到的信息 建议使用 参数num用于设置返回的数量 Return lastest messages, to prevent the msg_list being too long   Arg num is for set the number of returning message
    def get_latest_messages(self, num=1):
        return self.msg_list[:num]

    # todo
    #  add function for returning only groupchat message / only personalchat message / message for specific group or person

    ######## Send ########

    def send_http(self, uri, data):
        if isinstance(data, str) or isinstance(data, bytes):
            data = json.loads(data)
        base_data = {
            'id': getid(),
            'type': 'null',
            'roomid': 'null',
            'wxid': 'null',
            'content': 'null',
            'nickname': 'null',
            'ext': 'null',
        }
        base_data.update(data)
        url = f'http://{self.ip}:{self.port}/{uri}'
        try:
            rsp = requests.post(url, json={'para': base_data})
        except:
            print('发送信息失败！信息：', base_data)
        rsp = rsp.json()
        if 'content' in rsp and isinstance(rsp['content'], str):
            try:
                rsp['content'] = json.loads(rsp['content'])
            except:
                pass
        return rsp

    # 发送txt消息到个人或群 wxid为用户id或群id content为发送内容  Send txt message to a wxid(perosnal or group)
    def send_txt_msg(self, wxid, content: str):
        uri = '/api/sendtxtmsg'
        return self.send_http(uri, json_send_txt_msg(wxid, content))

    # 发送图片信息 wxid为用户id或群id path为发送图片的路径（建议用绝对路径） Send picture to wxid(perosnal or group)
    def send_pic_msg(self, wxid, path: str):
        uri = '/api/sendpic'
        return self.send_http(uri, json_send_pic_msg(wxid, path))

    # 发送@信息 roomid为群id wxid为用户id nickname为@的人昵称 content为发送内容 send @ message
    def send_at_msg(self, roomid, wxid, nickname: str, content: str):
        uri = '/api/sendatmsg'
        return self.send_http(uri, json_send_at_msg(roomid, wxid, nickname, content))

    # 发送文件 wxid为用户id或者群id path为文件的路径 send attachment to chat or group
    def send_attach_msg(self, wxid, path):
        uri = '/api/sendattatch'
        return self.send_http(uri, json_send_attach_msg(wxid, path))

    ######## 获取信息 ########

    # 获取唯一id
    def getid(self):
        return time.time_ns()

    def heartbeat(h):
        return h

    # 获取账号信息 wxid为用户id get other user's information
    def get_personal_detail(self, wxid):
        uri = '/api/get_personal_detail'
        return self.send_http(uri, json_get_personal_detail(wxid))

    # 获取登陆的账号信息 和get_personal_detail不同于get_personal_detail是获取其他用户的 get self's imformation
    # 接口有错误，暂时禁用
    '''    
    def get_personal_info(self):
        uri = '/api/get_personal_info'
        return self.send_http(uri, get_personal_info())'''

    # 获取微信通讯录用户名字和wxid get wechat address list username and wxid
    def get_contact_list(self):
        uri = '/api/getcontactlist'
        return self.send_http(uri, json_get_contact_list())

    # 获取群聊中用户昵称 wxid为群中要获取的用户id roomid为群id  get group's user's nickname
    def get_chatroom_nick(self, roomid='null', wxid='ROOT'):
        uri = 'api/getmembernick'
        return self.send_http(uri, json_get_chatroom_nick(roomid, wxid))

    # Alias of get_chat_nick
    def get_user_nick(self, wxid):
        return self.get_chatroom_nick(wxid=wxid)

    # 获取群聊中用户列表 wxid为群id
    def get_chatroom_memberlist(self, roomid='null'):
        uri = '/api/get_charroom_member_list'
        return self.send_http(uri, json_get_chatroom_memberlist(roomid))

    ######## 信息处理 ########

    def recv_txt_handle(self, recieve):
        out = {}
        out['content'] = recieve['content']
        out['id'] = recieve['id']
        out['time'] = recieve['time']
        out['type'] = recieve['type']
        out['wxid'] = recieve['wxid']
        out['nick'] = self.get_user_nick(recieve['wxid'])['content']['nick']
        return out
