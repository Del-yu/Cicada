# -*-* coding:utf-8 -*-*
import re
import os
import sys
import time
import asyncio
import requests
from queue import Queue
from conf import setting
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from multiprocessing.dummy import Process


def use_time(func):
    """ 计算使用时间 """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        stop_time = time.time()
        all_time = round(stop_time - start_time, 2)
        print(f'\r\033[0;34m[⇣]\033[0m Finished use time {all_time}s{20 * " "}')
        os._exit(0)

    return wrapper


def catch_exception(func):
    """ 捕获异常并记录 """

    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            self.signal.put({'style': 'error', 'message': e.args[0], 'finish': True})

    return wrapper


def check_input(match_name):
    """ 检查传入参数 """

    def inner(func):
        def wrapper(self, *args, **kwargs):
            if f"'{match_name}'" in str(self.target):
                func(self, self.target)
        return wrapper

    return inner


class Request(requests.Session):
    def __init__(self):
        super().__init__()
        self.timeout = setting.DEFAULT_REQUEST_TIMEOUT
        self.retries = setting.DEFAULT_REQUEST_RETRIES
        self.headers = setting.DEFAULT_REQUEST_HEADERS
        self.mount('http://', HTTPAdapter(max_retries=setting.DEFAULT_REQUEST_RETRIES))
        self.mount('https://', HTTPAdapter(max_retries=setting.DEFAULT_REQUEST_RETRIES))
        self.verify = False

    def request(self, method, url, *args, **kwargs):
        if setting.RANDOM_USER_AGENT:
            """ 随机UA """
            user_agent = UserAgent()
            self.headers.update({'User-Agent': user_agent.random})
        kwargs.update({'timeout': self.timeout})
        response = super().request(method, url, *args, **kwargs)
        return response


class Console:
    def __init__(self):
        self.RED = '\033[0;31m{}\033[0m'
        self.BLUE = '\033[0;34m{}\033[0m'
        self.YELLOW = '\033[0;33m{}\033[0m'
        self.GREEN = '\033[0;92m{}\033[0m'

    @staticmethod
    def print(style, message):
        print(f"\r{setting.PRINT_FORMAT[style] % {'message': message}}{30 * ' '}")

    @staticmethod
    def stdout(message):
        sys.stdout.write('\r\033[0;34m[{}]\033[0m {}'.format(['\\', '|', '/', '-'][int(time.time()) % 4], message))


class PluginBase(Request):
    def __init__(self):
        Request.__init__(self)


class PluginObject(dict):
    def __getattr__(self, item):
        return dict.__getitem__(self, item)


class FrameMain(Console):
    def __init__(self, options):
        Console.__init__(self)
        self.task = Queue()
        self.signal = Queue()
        self.options = options
        self.count = 0
        self.wait = {}
        self.plugin_count = 0

    def handle(self):
        """ 传入处理 """
        if self.options['input']:
            with open(self.options['input'], encoding='UTF-8-sig') as f:
                target_list = filter(lambda x: x != '', list(set(map(lambda x: x.strip(), f.readlines()))))
        else:
            target_list = [self.options['target']]
        for one_target in target_list:
            self.match(one_target)

    def match(self, one_target):
        """ 正则 自动识别 """
        if re.match(r'^1[35678]\d{9}$', one_target):
            self.task.put({'mobile': one_target, 'rate': 10, 'count': self.options['count']})
        elif re.match(r'^([\w]+\.*)([\w]+)\@[\w]+\.\w{3}(\.\w{2}|)$', one_target):
            self.task.put({'email': one_target, 'rate': 10, 'count': self.options['count']})
        else:
            raise Exception('Error: target is unavailable')

    def start(self):
        """ 开始方法 """
        self.handle()
        self.manager()

    def manager(self):
        try:
            putter_process = Process(target=self.put_queue)
            getter_process = Process(target=self.get_queue)
            putter_process.start()
            getter_process.start()
            putter_process.join()
        except Exception as e:
            raise Exception(e.args[0])

    def put_queue(self):
        one_target = self.task.get()
        if 'mobile' in one_target.keys():
            self.signal.put({'style': 'info', 'message': f"Target: {one_target['mobile']}"})
            target_type = 'mobile'
        else:
            self.signal.put({'style': 'info', 'message': f"Target: {one_target['email']}"})
            target_type = 'email'
        while True:
            self.bomb(one_target, target_type)

    @use_time
    def get_queue(self):
        while True:
            time.sleep(0.8)
            if not self.signal.empty():
                result = self.signal.get()
                if 'style' in result.keys() and 'message' in result.keys():
                    self.print(result['style'], result['message'])
                if 'finish' in result.keys():
                    break
            else:
                self.stdout('Please wait a moment')

    @catch_exception
    def bomb(self, target_data, target_type):
        plugin_list = [filename[:-3] for filename in os.listdir(os.path.join('plugins', target_type)) if
                       filename.endswith(".py") and not filename.startswith("_")]
        self.plugin_count = len(plugin_list)
        if self.plugin_count == 0:
            self.signal.put({'style': 'error', 'message': 'no plugins', 'finish': True})
        if self.options['plugin']:
            if self.options['plugin'] in plugin_list:
                plugin_list = [self.options['plugin']]
            else:
                self.signal.put(
                    {'style': 'error', 'message': f'plugin {self.options["plugin"]} is not available', 'finish': True})
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        semaphore = asyncio.Semaphore(setting.ASYNCIO_COUNT)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(
            *[self.async_task(target_data, target_type, plugin_name, semaphore) for plugin_name in plugin_list]))

    async def async_task(self, target_data, target_type, plugin_name, semaphore):
        async with semaphore:
            await asyncio.sleep(self.wait.get(plugin_name, 0))
            try:
                plugin_object = PluginObject({"Base": PluginBase})
                exec(open(os.path.join('plugins', target_type, plugin_name + '.py'), "rb").read(), plugin_object)
                result = plugin_object['Plugin']().start(target_data[target_type])
            except Exception as e:
                target_data['rate'] -= 1
                self.signal.put(
                    {'style': 'warn',
                     'message': f'Plugin {plugin_name} exception \033[0;31m{str(e)[:100]}\033[0m'})
            else:
                if result is not None:
                    self.wait[plugin_name] = result['wait']
                    target_data['rate'] = 10
                    message = '\033[0;32msuccess\033[0m'
                    target_data['count'] -= 1
                else:
                    target_data['rate'] -= 1
                    message = '\033[0;31mfailure\033[0m'
                self.signal.put({'style': 'right', 'message': f'Plugin {plugin_name} exec {message}'})
            if target_data['rate'] < 1:
                target_data['count'] -= 1
            if target_data['count'] < 1:
                self.signal.put({'finish': True})
