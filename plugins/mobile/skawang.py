# -*-* coding:utf-8 -*-*


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
