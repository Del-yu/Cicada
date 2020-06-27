# -*-* coding:utf-8 -*-*
"""
Name: 蝉鸣-信息轰炸工具
Author: Doimet
Data: 2020-03-15
"""
import os
import sys
import click
from conf import setting
import requests.packages.urllib3

os.system('')
sys.dont_write_bytecode = True
requests.packages.urllib3.disable_warnings()


def show_version(ctx, param, value):
    """ 显示程序版本 """
    if not value or ctx.resilient_parsing:
        return
    exit(f'Current version {setting.CURRENT_VERSION}')


@click.command()
@click.option('--input', '-i', help='从指定文件加载目标.')
@click.option('--target', '-t', help='设置信息轰炸的目标.')
@click.option('--count', '-c', help='设置信息轰炸的次数.', default=1)
@click.option('--plugin', '-p', help='调用指定插件去攻击.')
@click.option('--version', help='显示当前程序的版本.', is_flag=True, callback=show_version, expose_value=False,
              is_eager=True)
def cli(**kwargs):
    """ Easy to use Information bombardment tool """
    return main(kwargs)


def check_environment():
    """ 检测当前环境 """
    version = sys.version.split()[0]
    if version < '3.5':
        exit('Need python version > 3.5')


def show_banner():
    """ 打印Banner """
    banner = """
        \033[0;31mCicada bomb Tool v1.0\033[0m
    """
    print(f"""{banner}
 =# Author: Doimet
 =# Github: https://github.com/Doimet/Cicada
""")


def main(options):
    """ 程序的主函数 """
    show_banner()
    check_environment()
    try:
        from bins.cicada import FrameMain
        FrameMain(options).start()
    except Exception as e:
        exit(f"\033[0;31m[-]\033[0m {e}")


if __name__ == '__main__':
    cli()
