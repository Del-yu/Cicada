# -*-* coding:utf-8 -*-*

""" 当前版本 """
CURRENT_VERSION = 1.0

# ---------------------------------------------------------------------------
#   打印配置
# ---------------------------------------------------------------------------

PRINT_FORMAT = {
    "warn":  "\033[0;33m[!]\033[0m %(message)s",
    "info":  "\033[0;34m[+]\033[0m %(message)s",
    "error": "\033[0;31m[-]\033[0m %(message)s",
    "right": "\033[0;34m | \033[0m %(message)s",
}

# ---------------------------------------------------------------------------
#   网络配置
# ---------------------------------------------------------------------------

""" 默认HTTP请求头 """
DEFAULT_REQUEST_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
    "accept-language": "en-US,en;q=0.5",
    "cache-control": "no-cache",
    "connection": "close",
}

""" 默认请求超时时间 """
DEFAULT_REQUEST_TIMEOUT = 10

""" 默认请求重试次数 """
DEFAULT_REQUEST_RETRIES = 3

""" 随机UA开关 """
RANDOM_USER_AGENT = False

# ---------------------------------------------------------------------------
#   模块配置
# ---------------------------------------------------------------------------

""" 异步超时时间 """
ASYNCIO_TIMEOUT = 10

""" 异步并发量 """
ASYNCIO_COUNT = 300

""" 线程并发量 """
THREAD_COUNT = 200

