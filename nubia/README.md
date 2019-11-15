<h1 align="center"><a href="https://bbs.nubia.cn/">Nubia</a></h1>

## Installation

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements/development.txt
```

## Example
```python3
# 成功获取 https://bbs.nubia.cn/ 的响应

Python 3.7.4 (default, Jul  9 2019, 18:13:23)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.9.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from nubia.bbs import Nubia
In [2]: path = '/usr/local/opt/node@10/bin/node'
In [3]: bbs = Nubia(path=path)
In [4]: response = bbs.standard_request_bbs()
In [5]: '努比亚社区' in response.text
Out[5]: True
```

## 关于成功获取响应内容的详细步骤
- [nubia.bbs.Nubia](./nubia/bbs.py)
- [详细参考文章: 来自 悦来客栈的老板 , 十分感谢!!!](https://mp.weixin.qq.com/s/mZ-MBC2KbIlbXIKvamwq7Q)

## Thanks
QAQ
- [微信: 悦来客栈的老板](.)
