import websocket
from threading import Thread

class Pywxdll:
    def __init__(self, ip='127.0.0.1', port=5555, url='https://127.0.0.1:8888/wechat/msg/receiver/'):
        self.ws_url = f'ws://{ip}:{port}'
        self.url = url
        self.msg_list=[]

    def thread_start(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.run_forever()

    def start(self):
        wx = Pywxdll('127.0.0.1', port=5555, url='https://www.httpbin.org/anything')
        thread = Thread(target=wx.thread_start)
        thread.start()

    def on_open(self, ws):
        print('self', self)
        print('msglist',self.msg_list)
        print(f'{self.ws_url} opened successfully.')

    def on_message(self, ws, message):
        print(message)
        self.msg_list+=message

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, n1, n2):
        print(f'{self.ws_url} closed')

    def get_all_messages(self):
        return self.msg_list

    def get_latest_messages(self, num):
        return self.msg_list[:num]