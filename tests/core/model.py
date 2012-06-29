import unittest
import utils.model
from puremvc.core import Model
from puremvc.interfaces import IModel
from puremvc.patterns.proxy import Proxy

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
        """ModelTest: Test registerProxy() and retrieveProxy()"""
        model = Model('test')
        model.registerProxy(Proxy('colors', ['red', 'green', 'blue']))
        testProxy = model.retrieveProxy('colors')
        data = testProxy.getData()

        self.assertNotEqual(None, data)
        self.assertEqual(True, isinstance(data, list))
        self.assertEqual(True, len(data) == 3 )
        self.assertEqual(True, data[0]  == 'red' )
        self.assertEqual(True, data[1]  == 'green' )
        self.assertEqual(True, data[2]  == 'blue' )

    def testRegisterAndRemoveProxy(self):
        """ModelTest: Test registerProxy() and removeProxy()"""
        model = Model('test')
        testProxy = Proxy('sizes', ['7', '13', '21'])
        model.registerProxy(testProxy)

        removedProxy = model.removeProxy('sizes')

        self.assertEqual(True,removedProxy.getProxyName() == 'sizes')

        testProxy = model.retrieveProxy('sizes')

        self.assertEqual(None, testProxy)

    def testHasProxy(self):
        """ModelTest: Test hasProxy()"""

        model = Model('test')
        testProxy = Proxy('aces', ['clubs', 'spades', 'hearts', 'diamonds'])
        model.registerProxy(testProxy)

        self.assertEqual(True, model.hasProxy('aces'))

        model.removeProxy('aces')

        self.assertEqual(False, model.hasProxy('aces'))


    def testOnRegisterAndOnRemove(self):
        """ModelTest: Test onRegister() and onRemove()"""

        model = Model('test')

        testProxy = utils.model.ModelTestProxy()
        model.registerProxy(testProxy)

        self.assertEqual(True, testProxy.getData() == utils.model.ModelTestProxy.ON_REGISTER_CALLED)

        model.removeProxy(utils.model.ModelTestProxy.NAME)

        self.assertEqual(True, testProxy.getData() == utils.model.ModelTestProxy.ON_REMOVE_CALLED)
