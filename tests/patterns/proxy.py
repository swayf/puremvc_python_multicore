from puremvc_multicore.patterns.proxy import Proxy
from nose.tools import eq_, ok_

def testNameAccessor():
    """ProxyTest: Test Name Accessor"""

    prxy = Proxy('TestProxy')
    eq_(prxy.get_proxy_name(), 'TestProxy')

    class SuperTestProxy(Proxy):
        pass

    prxy = SuperTestProxy()
    eq_(prxy.get_proxy_name(), 'SuperTestProxy')


def testDataAccessors():
    """ProxyTest: Test Data Accessors"""

    prxy = Proxy('colors')
    prxy.set_data(['red', 'green', 'blue'])
    data = prxy.get_data()

    eq_(len(data), 3)
    eq_(data[0], 'red')
    eq_(data[1], 'green')
    eq_(data[2], 'blue')


def testConstructor():
    """ProxyTest: Test Constructor"""

    prxy = Proxy('colors',['red', 'green', 'blue'])
    data = prxy.get_data()

    ok_(prxy is not None)
    eq_(prxy.get_proxy_name(), 'colors')
    eq_(len(data), 3)
    eq_(data[0], 'red')
    eq_(data[1], 'green')
    eq_(data[2], 'blue')


