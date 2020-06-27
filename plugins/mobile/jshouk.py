# -*-* coding:utf-8 -*-*


class Plugin(Base):
    def __init__(self, *args):
        super().__init__(*args)

    def start(self, mobile: str):
        with self.get(f'http://www.jshouk.com/user/send.jhtml?mobile={mobile}') as r:
            if 'OK' in r.text:
                return {'status': True, 'wait': 0}
