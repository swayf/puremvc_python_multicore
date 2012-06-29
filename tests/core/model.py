import unittest
import utils.model
from puremvc_multicore.core import Model
from puremvc_multicore.interfaces import IModel
from puremvc_multicore.patterns.proxy import Proxy

class ModelTest(unittest.TestCase):
    """ModelTest: Test Model Singleton"""
    def assertNotNone(self):
        """ModelTest: Test instance not null"""
        model = Model('test')
        self.assertNotEqual(None, model)

    def assertIModel(self):
        """ModelTest: Test instance implements IModel"""
        model = Model('test')
        self.assertEqual(True, isinstance(model, IModel))

    def testRegisterAndRetrieveProxy(self):
        """ModelTest: Test register_proxy() and retrieve_proxy()"""
        model = Model('test')
        model.register_proxy(Proxy('colors', ['red', 'green', 'blue']))
        testProxy = model.retrieve_proxy('colors')
        data = testProxy.get_data()

        self.assertNotEqual(None, data)
        self.assertEqual(True, isinstance(data, list))
        self.assertEqual(True, len(data) == 3 )
        self.assertEqual(True, data[0]  == 'red' )
        self.assertEqual(True, data[1]  == 'green' )
        self.assertEqual(True, data[2]  == 'blue' )

    def testRegisterAndRemoveProxy(self):
        """ModelTest: Test register_proxy() and remove_proxy()"""
        model = Model('test')
        testProxy = Proxy('sizes', ['7', '13', '21'])
        model.register_proxy(testProxy)

        removedProxy = model.remove_proxy('sizes')

        self.assertEqual(True,removedProxy.get_proxy_name() == 'sizes')

        testProxy = model.retrieve_proxy('sizes')

        self.assertEqual(None, testProxy)

    def testHasProxy(self):
        """ModelTest: Test has_proxy()"""

        model = Model('test')
        testProxy = Proxy('aces', ['clubs', 'spades', 'hearts', 'diamonds'])
        model.register_proxy(testProxy)

        self.assertEqual(True, model.has_proxy('aces'))

        model.remove_proxy('aces')

        self.assertEqual(False, model.has_proxy('aces'))


    def testOnRegisterAndOnRemove(self):
        """ModelTest: Test on_register() and on_remove()"""

        model = Model('test')

        testProxy = utils.model.ModelTestProxy()
        model.register_proxy(testProxy)

        self.assertEqual(True, testProxy.get_data() == utils.model.ModelTestProxy.ON_REGISTER_CALLED)

        model.remove_proxy(utils.model.ModelTestProxy.NAME)

        self.assertEqual(True, testProxy.get_data() == utils.model.ModelTestProxy.ON_REMOVE_CALLED)
