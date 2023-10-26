# `pip install pywxdll`
# pywxdll

A Python package for wechat dll hook 一个用于微信Dll Hook的Python库

## For start

Currently writing documents, please use docker env(link: https://github.com/ChisBread/wechat-service/)

请在这个docker环境下运行：https://github.com/ChisBread/wechat-service/

## 如何使用

简单例子

```python
import pywxdll

bot = pywxdll.Pywxdll('127.0.0.1', 5555)
bot.start()
print(bot.get_contact_list())
```

## Credits

https://github.com/ChisBread/wechat-service/

https://github.com/cixingguangming55555/wechat-bot

https://github.com/chisbread/wechat-box
