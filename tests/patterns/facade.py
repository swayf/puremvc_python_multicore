import unittest
import utils.facade
from puremvc_multicore.interfaces import IFacade, IProxy
from puremvc_multicore.patterns.facade import Facade
from puremvc_multicore.patterns.mediator import Mediator
from puremvc_multicore.patterns.proxy import Proxy

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
        """FacadeTest: Test register_command() and send_notification()"""

        fcde = Facade('test')
        fcde.register_command('FacadeTestNote', utils.facade.FacadeTestCommand)

        vo = utils.facade.FacadeTestVO(32)
        fcde.send_notification('FacadeTestNote', vo)

        self.assertEqual(True, vo.result == 64)

    def testRegisterAndRemoveCommandAndSendNotification(self):
        """FacadeTest: Test remove_command() and subsequent send_notification()"""
        fcde = Facade('test')
        fcde.register_command('FacadeTestNote', utils.facade.FacadeTestCommand)
        fcde.remove_command('FacadeTestNote')

        vo = utils.facade.FacadeTestVO(32)
        fcde.send_notification('FacadeTestNote', vo)

        self.assertEqual(True, vo.result != 64)

    def testRegisterAndRetrieveProxy(self):
        """FacadeTest: Test register_proxy() and retrieve_proxy()"""
        fcde = Facade('test')
        fcde.register_proxy(Proxy('colors', ['red', 'green', 'blue']))
        pxy = fcde.retrieve_proxy('colors')

        self.assertEqual(True, isinstance(pxy, IProxy))

        data = pxy.get_data()

        self.assertEqual(True, data is not None)
        self.assertEqual(True, isinstance(data, list))
        self.assertEqual(True, len(data) == 3)
        self.assertEqual(True, data[0]  == 'red')
        self.assertEqual(True, data[1]  == 'green')
        self.assertEqual(True, data[2]  == 'blue')

    def testRegisterAndRemoveProxy(self):
        """FacadeTest: Test register_proxy() and remove_proxy()"""

        fcde = Facade('test')
        pxy = Proxy('sizes', ['7', '13', '21'])
        fcde.register_proxy(pxy)

        removedProxy = fcde.remove_proxy('sizes')

        self.assertEqual(True, removedProxy.get_proxy_name() == 'sizes')

        pxy = fcde.retrieve_proxy('sizes')

        self.assertEqual(True, pxy is None)

    def testRegisterRetrieveAndRemoveMediator(self):
        """FacadeTest: Test register_mediator() retrieve_mediator() and remove_mediator()"""

        fcde = Facade('test')
        fcde.register_mediator(Mediator(Mediator.NAME, object()))

        self.assertEqual(True, fcde.retrieve_mediator(Mediator.NAME) is not None)

        removedMediator = fcde.remove_mediator(Mediator.NAME)

        self.assertEqual(True, removedMediator.get_mediator_name() == Mediator.NAME)

        self.assertEqual(True, fcde.retrieve_mediator(Mediator.NAME) is None)

    def testHasProxy(self):
        """FacadeTest: Test has_proxy()"""

        fcde = Facade('test')
        fcde.register_proxy(Proxy('hasProxyTest', [1,2,3]))

        self.assertEqual(True, fcde.has_proxy('hasProxyTest'))

        fcde.remove_proxy('hasProxyTest')

        self.assertEqual(False, fcde.has_proxy('hasProxyTest'))

    def testHasMediator(self):
        """FacadeTest: Test has_mediator()"""

        fcde = Facade('test')
        fcde.register_mediator(Mediator('facadeHasMediatorTest', object()))

        self.assertEqual(True, fcde.has_mediator('facadeHasMediatorTest'))

        fcde.remove_mediator('facadeHasMediatorTest')

        self.assertEqual(False, fcde.has_mediator('facadeHasMediatorTest'))

    def testHasCommand(self):
        """FacadeTest: Test has_command()"""
        fcde = Facade('test')
        fcde.register_command('facadeHasCommandTest', utils.facade.FacadeTestCommand)

        self.assertEqual(True, fcde.has_command('facadeHasCommandTest'))

        fcde.remove_command('facadeHasCommandTest')

        self.assertEqual(False, fcde.has_command('facadeHasCommandTest'))


