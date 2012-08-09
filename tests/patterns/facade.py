from nose.tools import eq_,ok_
import utils.facade
from puremvc_multicore.interfaces import IFacade, IProxy
from puremvc_multicore.patterns.facade import Facade
from puremvc_multicore.patterns.mediator import Mediator
from puremvc_multicore.patterns.proxy import Proxy


def assertNotNone():
    """FacadeTest: Test instance not null"""
    fcde = Facade('test')
    ok_(fcde is not None)


def assertIFacade():
    """FacadeTest: Test instance implements IFacade"""
    fcde = Facade('test')
    ok_(isinstance(fcde, IFacade))


def testRegisterCommandAndSendNotification():
    """FacadeTest: Test register_command() and send_notification()"""
    fcde = Facade('test')
    fcde.register_command('FacadeTestNote', utils.facade.FacadeTestCommand)

    vo = utils.facade.FacadeTestVO(32)
    fcde.send_notification('FacadeTestNote', vo)

    eq_(vo.result, 64)


def testRegisterAndRemoveCommandAndSendNotification():
    """FacadeTest: Test remove_command() and subsequent send_notification()"""
    fcde = Facade('test')
    fcde.register_command('FacadeTestNote', utils.facade.FacadeTestCommand)
    fcde.remove_command('FacadeTestNote')

    vo = utils.facade.FacadeTestVO(32)
    fcde.send_notification('FacadeTestNote', vo)

    ok_(vo.result != 64)


def testRegisterAndRetrieveProxy():
    """FacadeTest: Test register_proxy() and retrieve_proxy()"""
    fcde = Facade('test')
    fcde.register_proxy(Proxy('colors', ['red', 'green', 'blue']))
    pxy = fcde.retrieve_proxy('colors')

    ok_(isinstance(pxy, IProxy))

    data = pxy.get_data()

    ok_(data is not None)
    ok_(isinstance(data, list))
    eq_(len(data), 3)
    eq_(data[0], 'red')
    eq_(data[1], 'green')
    eq_(data[2], 'blue')


def testRegisterAndRemoveProxy():
    """FacadeTest: Test register_proxy() and remove_proxy()"""
    fcde = Facade('test')
    pxy = Proxy('sizes', ['7', '13', '21'])
    fcde.register_proxy(pxy)

    removedProxy = fcde.remove_proxy('sizes')
    eq_(removedProxy.get_proxy_name(), 'sizes')

    pxy = fcde.retrieve_proxy('sizes')
    ok_(pxy is None)




def testRegisterRetrieveAndRemoveMediator():
    """FacadeTest: Test register_mediator() retrieve_mediator() and remove_mediator()"""
    fcde = Facade('test')
    fcde.register_mediator(Mediator(view_component=object()))
    ok_(fcde.retrieve_mediator('Mediator') is not None)

    removedMediator = fcde.remove_mediator('Mediator')
    eq_(removedMediator.get_mediator_name(), 'Mediator')
    ok_(fcde.retrieve_mediator(Mediator.NAME) is None)


def testHasProxy():
    """FacadeTest: Test has_proxy()"""
    fcde = Facade('test')
    fcde.register_proxy(Proxy('hasProxyTest', [1,2,3]))
    ok_(fcde.has_proxy('hasProxyTest'))

    fcde.remove_proxy('hasProxyTest')
    ok_(not fcde.has_proxy('hasProxyTest'))


def testHasMediator():
    """FacadeTest: Test has_mediator()"""
    fcde = Facade('test')
    fcde.register_mediator(Mediator('facadeHasMediatorTest', object()))
    ok_(fcde.has_mediator('facadeHasMediatorTest'))

    fcde.remove_mediator('facadeHasMediatorTest')
    ok_(not fcde.has_mediator('facadeHasMediatorTest'))


def testHasCommand():
    """FacadeTest: Test has_command()"""
    fcde = Facade('test')
    fcde.register_command('facadeHasCommandTest', utils.facade.FacadeTestCommand)
    ok_(fcde.has_command('facadeHasCommandTest'))

    fcde.remove_command('facadeHasCommandTest')
    ok_(not fcde.has_command('facadeHasCommandTest'))


