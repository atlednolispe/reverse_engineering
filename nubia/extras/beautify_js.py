# -*- coding: utf-8 -*-

"""
调用PyExecJS简化代码以及生成acw_sc__v2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

from typing import Optional
import _io
import os
import re

import execjs


class Beautify:
    def __init__(self: 'Beautify', path: str = '/usr/local/opt/node@10/bin/node') -> None:
        """实例化一个Beautify对象

        :param path: str, js interpreter 的PATH路径, 需要传入测试电脑的对应PATH路径
        """
        self.path: str = path
        os.environ["EXECJS_RUNTIME"] = path
        self.node: execjs._external_runtime.ExternalRuntime = execjs.get()
        self._function__0x55f3_runtime: Optional[execjs._external_runtime.ExternalRuntime.Context] = None
        self._function_v2_runtime: Optional[execjs._external_runtime.ExternalRuntime.Context] = None

    @property
    def _0x55f3_runtime(self: 'Beautify') -> execjs._external_runtime.ExternalRuntime.Context:
        """获取_0x55f3的runtime

        :return: execjs._external_runtime.ExternalRuntime.Context, _0x55f3的runtime
        """
        if self._function__0x55f3_runtime is None:
            js_path = 'static/_0x55f3_for_execjs.js'
            self._0x55f3_runtime = js_path
        return self._function__0x55f3_runtime

    @_0x55f3_runtime.setter
    def _0x55f3_runtime(self: 'Beautify', js_path='static/_0x55f3_for_execjs.js') -> None:
        """设置_0x55f3的runtime

        :param js_path: str, _0x55f3函数的js文件路径
        :return: None
        """
        f: _io.TextIOWrapper
        with open(js_path) as f:
            js: str = f.read()
        self._function__0x55f3_runtime = self.node.compile(js)

    def function__0x55f3(self: 'Beautify', x: str, y: str) -> str:
        """返回_0x55f3的执行结果

        :param x: str, 传递给_0x55f3的第一个参数
        :param y: str, 传递给_0x55f3的第二个参数
        :return: str, _0x55f3的执行结果
        """
        return self._0x55f3_runtime.call('_0x55f3', x, y)

    def generate_cleaned_bbs_js(self: 'Beautify') -> None:
        """生成简化后的cleaned_bbs.js

        static/after__0x55f3.js: _0x55f3函数后面部分的bbs.js
        static/cleaned__0x55f3.js: 人肉简化后的_0x55f3
        static/cleaned_bbs.js: 简化后的bbs.js
        static/ultimate_bbs.js: 最终用于调用生成acw_sc__v2的js

        :return: None
        """
        with open('static/after__0x55f3.js') as f_bbs:
            after = f_bbs.read()
        pattern = re.compile(r"_0x55f3\('(.*?)', '(.*?)'\)")
        encrypted = pattern.findall(after)
        for param_x, param_y in encrypted:
            after = after.replace(f"_0x55f3('{param_x}', '{param_y}')", f"'{self.function__0x55f3(param_x, param_y)}'")
        with open('static/cleaned__0x55f3.js') as f_0x55fc:
            before = f_0x55fc.read()
        with open('static/cleaned_bbs.js', 'w', encoding='utf-8') as f_cleaned:
            f_cleaned.write(before)
            f_cleaned.write(after)

    @property
    def v2_runtime(self: 'Beautify') -> execjs._external_runtime.ExternalRuntime.Context:
        """获取v2的runtime

        :return: execjs._external_runtime.ExternalRuntime.Context, _0x55f3的runtime
        """
        if self._function_v2_runtime is None:
            raise Exception('v2_runtime is not setted, exec: Nubia().v2_runtime = arg1 / None first plz!!!')
        return self._function_v2_runtime

    @v2_runtime.setter
    def v2_runtime(self: 'Beautify', arg1: Optional[str] = None) -> None:
        """设置v2的runtime

        :param arg1: Optional[str], 首次请求nubia返回的js中的arg1的值, 若为None则使用默认的arg1
        :return: None
        """
        default_arg1: str = '0F6D28AF88D56E6A0B09E8439F72C72EE0DC5D45'
        f: _io.TextIOWrapper
        with open('static/ultimate_bbs.js') as f:
            js: str = f.read()
        if arg1 is not None:
            js = js.replace(default_arg1, arg1)

        self._function_v2_runtime = self.node.compile(js)

    def function_v2(self: 'Beautify') -> str:
        """返回cookies中acw_sc__v2的对应值

        :return: str, acw_sc__v2
        """
        v2_runtime = self.v2_runtime
        return v2_runtime.call('v2')
