import unittest
import utils.facade
from puremvc.interfaces import IFacade, IProxy
from puremvc.patterns.facade import Facade
from puremvc.patterns.mediator import Mediator
from puremvc.patterns.proxy import Proxy

class FacadeTest(unittest.TestCase):
    """FacadeTest: Test Facade Pattern"""

    def assertNotNone(self):
        """FacadeTest: Test instance not null"""
        fcde = Facade('test')
        self.assertNotEqual(None, fcde)

    def assertIFacade(self):
        """FacadeTest: Test instance implements IFacade"""
        fcde = Facade('test')
        self.assertEqual(True, isinstance(fcde, IFacade))

    def testRegisterCommandAndSendNotification(self):
        """FacadeTest: Test registerCommand() and sendNotification()"""

        fcde = Facade('test')
        fcde.registerCommand('FacadeTestNote', utils.facade.FacadeTestCommand)

        vo = utils.facade.FacadeTestVO(32)
        fcde.sendNotification('FacadeTestNote', vo)

        self.assertEqual(True, vo.result == 64)

    def testRegisterAndRemoveCommandAndSendNotification(self):
        """FacadeTest: Test removeCommand() and subsequent sendNotification()"""
        fcde = Facade('test')
        fcde.registerCommand('FacadeTestNote', utils.facade.FacadeTestCommand)
        fcde.removeCommand('FacadeTestNote')

        vo = utils.facade.FacadeTestVO(32)
        fcde.sendNotification('FacadeTestNote', vo)

        self.assertEqual(True, vo.result != 64)

    def testRegisterAndRetrieveProxy(self):
        """FacadeTest: Test registerProxy() and retrieveProxy()"""
        fcde = Facade('test')
        fcde.registerProxy(Proxy('colors', ['red', 'green', 'blue']))
        pxy = fcde.retrieveProxy('colors')

        self.assertEqual(True, isinstance(pxy, IProxy))

        data = pxy.getData()

        self.assertEqual(True, data is not None)
        self.assertEqual(True, isinstance(data, list))
        self.assertEqual(True, len(data) == 3)
        self.assertEqual(True, data[0]  == 'red')
        self.assertEqual(True, data[1]  == 'green')
        self.assertEqual(True, data[2]  == 'blue')

    def testRegisterAndRemoveProxy(self):
        """FacadeTest: Test registerProxy() and removeProxy()"""

        fcde = Facade('test')
        pxy = Proxy('sizes', ['7', '13', '21'])
        fcde.registerProxy(pxy)

        removedProxy = fcde.removeProxy('sizes')

        self.assertEqual(True, removedProxy.getProxyName() == 'sizes')

        pxy = fcde.retrieveProxy('sizes')

        self.assertEqual(True, pxy is None)

    def testRegisterRetrieveAndRemoveMediator(self):
        """FacadeTest: Test registerMediator() retrieveMediator() and removeMediator()"""

        fcde = Facade('test')
        fcde.registerMediator(Mediator(Mediator.NAME, object()))

        self.assertEqual(True, fcde.retrieveMediator(Mediator.NAME) is not None)

        removedMediator = fcde.removeMediator(Mediator.NAME)

        self.assertEqual(True, removedMediator.getMediatorName() == Mediator.NAME)

        self.assertEqual(True, fcde.retrieveMediator(Mediator.NAME) is None)

    def testHasProxy(self):
        """FacadeTest: Test hasProxy()"""

        fcde = Facade('test')
        fcde.registerProxy(Proxy('hasProxyTest', [1,2,3]))

        self.assertEqual(True, fcde.hasProxy('hasProxyTest'))

        fcde.removeProxy('hasProxyTest')

        self.assertEqual(False, fcde.hasProxy('hasProxyTest'))

    def testHasMediator(self):
        """FacadeTest: Test hasMediator()"""

        fcde = Facade('test')
        fcde.registerMediator(Mediator('facadeHasMediatorTest', object()))

        self.assertEqual(True, fcde.hasMediator('facadeHasMediatorTest'))

        fcde.removeMediator('facadeHasMediatorTest')

        self.assertEqual(False, fcde.hasMediator('facadeHasMediatorTest'))

    def testHasCommand(self):
        """FacadeTest: Test hasCommand()"""
        fcde = Facade('test')
        fcde.registerCommand('facadeHasCommandTest', utils.facade.FacadeTestCommand)

        self.assertEqual(True, fcde.hasCommand('facadeHasCommandTest'))

        fcde.removeCommand('facadeHasCommandTest')

        self.assertEqual(False, fcde.hasCommand('facadeHasCommandTest'))


