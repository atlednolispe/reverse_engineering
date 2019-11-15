# -*- coding: utf-8 -*-

"""
获取请求的正确html响应
~~~~~~~~~~~~~~~~~~~

目标链接地址: https://bbs.nubia.cn/
参考: https://mp.weixin.qq.com/s/mZ-MBC2KbIlbXIKvamwq7Q

Core:
    1. Add conditional breakpoint 无法跳出 `debugger`,查看call stack发现`递归函数`, 将递归函数置空
    2. 服务器端有 Set-Cookie 操作,为正确拿到结果需要有前置请求
    3. 需要转义js代码中的字符串(https://beautifier.io/) xNN or uNNNN
    4. 关注函数调用是否改变实参数和全局变量, 并且关注函数的返回值 (便于去除多余代码)
    5. 替换一些混淆代码(例如解密字符串函数),使代码结构更清晰
    6. PyExecJS碰到浏览器自带函数缺失

Usage::
Python 3.7.4 (default, Jul  9 2019, 18:13:23)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.9.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from nubia.bbs import Nubia
In [2]: path = '/usr/local/opt/node@10/bin/node'
In [3]: bbs = Nubia(path=path)
In [4]: response = bbs.standard_request_bbs()
In [5]: '努比亚社区' in response.text
Out[5]: True
"""

from typing import Dict
import re
import time

import requests

from extras.beautify_js import Beautify


class Nubia:
    def __init__(self: 'Nubia', path: str = '/usr/local/opt/node@10/bin/node') -> None:
        """初始化Nubia实例

        :param path: PyExecJS 调用的 javascript interpreter 的 PATH, 需要传入测试电脑的对应PATH路径
        """
        self.headers: Dict = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36'
        }
        self.session: requests.Session = requests.Session()
        self.session.headers = self.headers
        self.path = path

    def _request_bbs(self: 'Nubia') -> requests.Response:
        """请求 https://bbs.nubia.cn/

        首次请求: 服务器端Set-Cookie: aliyungf_tc, acw_tc, 并且获取acw_sc__v2的js内容,
        第二次请求: (且携带完整所需的cookies)获取正确内容

        :return: requests.Response,
        """
        url: str = 'https://bbs.nubia.cn/'
        response: requests.Response = self.session.get(url)
        return response

    def _request_favicon(self: 'Nubia') -> None:
        """Cookies携带acw_tc, aliyungf_tc, 服务端Set-Cookie: acw_sc__v3 且 302后服务端Set-Cookie: SERVERID

        :return: None
        """
        url: str = 'https://bbs.nubia.cn/favicon.ico'
        favicon_response: requests.Response = self.session.get(url)

    def _add_acw_sc__v2_to_session(self: 'Nubia', pre_response: requests.Response) -> None:
        """首次请求的响应中会通过js Set-Cookie: acw_sc__v2, 通过Python模拟实现加密过程

        var arg1 = '0F6D28AF88D56E6A0B09E8439F72C72EE0DC5D45';

        var _0x4818 = ['csKHwqMI', ...];

        (function(_0x4c97f0, _0x1742fd) {...} (_0x4818, 0x15b));
        # 0x15b = 347
        _0x4818 这个数组要被shift - push: 347次, len(_0x4818) = 56, 最终_0x4818 = _0x4818[11:] + _0x4818[:11]

        var _0x55f3 = function(_0x4c97f0, _0x1742fd) {...};
        关注 _0x55f3 的返回值 以及 _0x55f3['xxx'] = yyy, 将函数最终简化为:
        var _0x55f3 = function(_0x4c97f0, _0x1742fd) {
            var _0x4c97f0 = parseInt(_0x4c97f0, 0x10);
            var _0x48181e = _0x4818[_0x4c97f0];
            var _0x232678 = function(_0x401af1, _0x532ac0) {...};
            _0x48181e = _0x232678(_0x48181e, _0x1742fd);
            return _0x48181e;
        };

        var arg3, ..., arg10 = null;

        将涉及 _0x55f3 的部分还原,比较好的办法是通过直接调用javascript来还原,其实也就涉及一些正则匹配之类的操作
        使用PyExecJS会有大坑,需要正确替换atob函数

        通过调用 Beautify 实例的 generate_cleaned_bbs_js 生成简化后的 cleaned_bbs.js

        最后去除部分与cookies中的acw_sc__v2 (即arg2) 无关的部分代码后为最终的 ultimate_bbs.js

        :return: None
        """
        arg1: str = self.__parse_arg1_from_pre_request(pre_response)
        # 需要传入测试电脑的对应js interpreter PATH路径
        beautify: Beautify = Beautify(path=self.path)
        beautify.v2_runtime = arg1
        acw_sc__v2: str = beautify.function_v2()
        expires: int = int(time.time()) + 3600 * 1000
        # var expiredate = new Date();
        # expiredate.setTime(expiredate.getTime() + (3600 * 1000));
        # document.cookie = name + "=" + value + ";expires=" + expiredate.toGMTString() + ";max-age=3600;path=/";
        cookie_acw_sc__v2: Dict = {
            'name': 'acw_sc__v2',
            'value': acw_sc__v2,
            'expires': expires,
            # 'max-age': '3600',  # 没有找到对应值
            'path': '/',

        }
        self.session.cookies.set(**cookie_acw_sc__v2)

    def __parse_arg1_from_pre_request(self: 'Nubia', response: requests.Response):
        """从首次响应中提取出变化的arg1字符串的内容用于后面生成所必需的cookie

        :param response: requests.Response, 首次请求 'https://bbs.nubia.cn/' 的响应
        :return: str, 每次变化的arg1,用于生成正确响应所必须的cookies中的acw_sc__v2
        """
        pattern_arg1: re.Pattern = re.compile("arg1='(.*?)'")
        arg1: str = pattern_arg1.findall(response.text)[0]
        return arg1

    def standard_request_bbs(self: 'Nubia') -> requests.Response:
        """可以拿到正确响应结果的请求

        Cookies中需要携带以下五个参数才可以获取正确响应:
            SERVERID, acw_sc__v2, acw_sc__v3, acw_tc, aliyungf_tc

        :return: requests.Response, 成功的响应结果
        """
        pre_response: requests.Response = self._request_bbs()
        self._request_favicon()
        self._add_acw_sc__v2_to_session(pre_response)
        standard_response: requests.Response = self._request_bbs()
        return standard_response
