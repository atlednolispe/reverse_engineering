from nubia.bbs import Nubia


class TestNubia:
    def test_bbs(self: 'TestNubia') -> None:
        """测试能否获取正确的响应

        :return: None
        """
        path = '/usr/local/opt/node@10/bin/node'
        nubia = Nubia(path=path)
        response = nubia.standard_request_bbs()
        assert '努比亚社区' in response.text
