# -*-* coding:utf-8 -*-*


class Plugin(Base):
    def __init__(self, *args):
        super().__init__(*args)

    def start(self, mobile: str):
        with self.post('http://www.yishiyigong.com/Admin/API/getVerifyCode.html', data={'mobile': mobile}) as r:
            if '\u53d1\u9001\u6210\u529f' in r.text:
                return {'status': True, 'wait': 60}
