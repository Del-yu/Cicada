# -*-* coding:utf-8 -*-*


class Plugin(Base):
    def __init__(self, *args):
        super().__init__(*args)

    def start(self, mobile: str):
        with self.get(f'http://m.10010.com/mall-mobile/CheckMessage/captcha?phoneVal={mobile}&type=1') as r:
            if 'null' in r.text:
                return {'wait': 60}
