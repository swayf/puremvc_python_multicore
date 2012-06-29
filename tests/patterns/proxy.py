import unittest
from puremvc_multicore.patterns.proxy import Proxy


class ProxyTest(unittest.TestCase):
    """ProxyTest: Test Proxy Pattern"""

    def testNameAccessor(self):
        """ProxyTest: Test Name Accessor"""

        prxy = Proxy('TestProxy')
        self.assertEqual(True, prxy.get_proxy_name() == 'TestProxy')

    def testDataAccessors(self):
        """ProxyTest: Test Data Accessors"""

        prxy = Proxy('colors')
        prxy.set_data(['red', 'green', 'blue'])
        data = prxy.get_data()

        self.assertEqual(True, len(data) == 3)
        self.assertEqual(True, data[0]  == 'red')
        self.assertEqual(True, data[1]  == 'green')
        self.assertEqual(True, data[2]  == 'blue')

    def testConstructor(self):
        """ProxyTest: Test Constructor"""

        prxy = Proxy('colors',['red', 'green', 'blue'])
        data = prxy.get_data()

        self.assertEqual(True, prxy is not None)
        self.assertEqual(True, prxy.get_proxy_name() == 'colors')
        self.assertEqual(True, len(data) == 3)
        self.assertEqual(True, data[0]  == 'red')
        self.assertEqual(True, data[1]  == 'green')
        self.assertEqual(True, data[2]  == 'blue')
