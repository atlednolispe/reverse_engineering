import pytest

from extras.beautify_js import Beautify


class TestBeautify:
    @pytest.fixture()
    def init_instance(self: 'TestBeautify') -> None:
        """测试预处理,生成Beautify实例

        :return: None
        """
        node_path: str = '/usr/local/opt/node@10/bin/node'
        self.beautify: Beautify = Beautify(path=node_path)

    @pytest.mark.usefixtures('init_instance')
    def test_function__0x55f3(self: 'TestBeautify') -> None:
        """测试PyExecJS调用的 _0x55f3 是否符合要求

        :return: None
        """
        assert self.beautify.function__0x55f3('0x36', 'yApz') == 'attachEvent'
