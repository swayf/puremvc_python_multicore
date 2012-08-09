from nose.tools import *
from puremvc_multicore.patterns.facade import Facade
from puremvc_multicore.patterns.proxy import Proxy


class CustomFacade(Facade):
    pass


def test_custom_facade():
    f1 = CustomFacade('test_1')
    f2 = Facade('test_1')
    f3 = CustomFacade('test_2')

    ok_(f1 is f2)
    ok_(f2 is not f3)


class CustomProxy(Proxy):
    def get_data(self):
        return 5


def test_register_retrieve_and_remove_proxy():
    """FacadeTest: Test register_proxy() and remove_proxy()"""
    facade = Facade('test_register_retrieve_and_remove_proxy')

    facade.register_proxy(CustomProxy())

    proxy = facade.retrieve_proxy('CustomProxy')
    eq_(proxy.get_data(), 5)

    removedProxy = facade.remove_proxy('CustomProxy')
    eq_(removedProxy.get_proxy_name(), 'CustomProxy')

    proxy = facade.retrieve_proxy('CustomProxy')
    ok_(proxy is None)


class CustomFacade(Facade):
    def register_proxy(self, proxy):
        if proxy.proxy_name == proxy.__class__.__name__:
            proxy.proxy_name = '_' + proxy.proxy_name + '_'
        super(CustomFacade, self).register_proxy(proxy)


def test_custom_facade_proxy():
    facade = CustomFacade('test_custom_facade_proxy')
    facade.register_proxy(CustomProxy())
    proxy = facade.retrieve_proxy('_CustomProxy_')
    eq_(proxy.get_data(), 5)