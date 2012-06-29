import unittest
import utils.view
from puremvc_multicore.core import View
from puremvc_multicore.interfaces import IView
from puremvc_multicore.patterns.mediator import Mediator
from puremvc_multicore.patterns.observer import Observer, Notification


class ViewTest(unittest.TestCase):
    """ViewTest: Test View Singleton"""

    lastNotification = None
    onRegisterCalled = False
    onRemoveCalled = False
    counter = 0

    NOTE1 = "note1"
    NOTE2 = "note2"
    NOTE3 = "note3"
    NOTE5 = "note5"

    def __cleanup(self):
        View('test').remove_mediator(utils.view.ViewTestMediator.NAME)
        View('test').remove_mediator(utils.view.ViewTestMediator2.NAME)
        View('test').remove_mediator(utils.view.ViewTestMediator3.NAME)
        View('test').remove_mediator(utils.view.ViewTestMediator4.NAME)
        View('test').remove_mediator(utils.view.ViewTestMediator5.NAME)

    def assertNotNone(self):
        """ViewTest: Test instance not null"""
        view = View('test')
        self.assertNotEqual(None, view)

    def assertIView(self):
        """ViewTest: Test instance implements IView"""
        view = View('test')
        self.assertEqual(True, isinstance(view, IView))

    def testRegisterAndNotifyObserver(self):
        """ViewTest: Test register_observer() and notify_observers()"""

        self.viewTestVar = 0
        def viewTestMethod(note):
            self.viewTestVar = note.get_body()

        view = View('test')
        obsvr = Observer(viewTestMethod, self)
        view.register_observer(utils.view.ViewTestNote.NAME, obsvr)

        note = utils.view.ViewTestNote.create(10)
        view.notify_observers(note)

        self.assertEqual(True, self.viewTestVar == 10)

    def testRegisterAndRetrieveMediator(self):
        """ViewTest: Test register_mediator() and retrieve_mediator()"""
        view = View('test')

        viewTestMediator = utils.view.ViewTestMediator(self)
        view.register_mediator(viewTestMediator)

        mediator = view.retrieve_mediator(utils.view.ViewTestMediator.NAME)

        self.assertEqual(True, isinstance(mediator, utils.view.ViewTestMediator))
        self.__cleanup()

    def testHasMediator(self):
        """ViewTest: Test has_mediator()"""
        view = View('test')
        meditr = Mediator('hasMediatorTest', self)
        view.register_mediator(meditr)

        self.assertEqual(True, view.has_mediator('hasMediatorTest'))

        view.remove_mediator('hasMediatorTest')

        self.assertEqual(False, view.has_mediator('hasMediatorTest'))
        self.__cleanup()

    def testRegisterAndRemoveMediator(self):
        """ViewTest: Test register_mediator() and remove_mediator()"""
        view = View('test')

        meditr = Mediator('testing', self)
        view.register_mediator(meditr)

        removedMediator = view.remove_mediator('testing')

        self.assertEqual(True, removedMediator.get_mediator_name() == 'testing')

        self.assertEqual(True, view.retrieve_mediator('testing') is None)
        self.__cleanup()

    def testOnRegisterAndOnRemove(self):
        """ViewTest: Test onRegsiter() and on_remove()"""
        view = View('test')

        mediator = utils.view.ViewTestMediator4(self)
        view.register_mediator(mediator)

        self.assertEqual(True, self.onRegisterCalled)

        view.remove_mediator(utils.view.ViewTestMediator4.NAME)

        self.assertEqual(True, self.onRemoveCalled)
        self.__cleanup()


    def testSuccessiveRegisterAndRemoveMediator(self):
        """ViewTest: Test Successive register_mediator() and remove_mediator()"""
        view = View('test')

        view.register_mediator(utils.view.ViewTestMediator(self))

        self.assertEqual(True, isinstance(view.retrieve_mediator(utils.view.ViewTestMediator.NAME), utils.view.ViewTestMediator))

        view.remove_mediator(utils.view.ViewTestMediator.NAME)

        self.assertEqual(True, view.retrieve_mediator(utils.view.ViewTestMediator.NAME) is None)

        self.assertEqual(True, view.remove_mediator(utils.view.ViewTestMediator.NAME) is None)

        view.register_mediator(utils.view.ViewTestMediator(self))

        self.assertEqual(True, isinstance(view.retrieve_mediator(utils.view.ViewTestMediator.NAME), utils.view.ViewTestMediator))

        view.remove_mediator(utils.view.ViewTestMediator.NAME)

        self.assertEqual(True, view.retrieve_mediator(utils.view.ViewTestMediator.NAME) is None)

        self.__cleanup()

    def testRemoveMediatorAndSubsequentNotify(self):
        """ViewTest: Test remove_mediator() and subsequent nofity()"""

        view = View('test')

        view.register_mediator(utils.view.ViewTestMediator2(self))

        view.notify_observers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification == self.NOTE1)

        view.notify_observers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification == self.NOTE2)

        view.remove_mediator(utils.view.ViewTestMediator2.NAME)

        self.assertEqual(True, view.retrieve_mediator(utils.view.ViewTestMediator2.NAME) is None)

        self.lastNotification = None

        view.notify_observers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification != self.NOTE1)

        view.notify_observers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification != self.NOTE2)

        self.__cleanup()

    def testRemoveOneOfTwoMediatorsAndSubsequentNotify(self):
        """ViewTest: Test removing one of two Mediators and subsequent notify()"""

        view = View('test')

        view.register_mediator(utils.view.ViewTestMediator2(self))

        view.register_mediator(utils.view.ViewTestMediator3(self))

        view.notify_observers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification == self.NOTE1)

        view.notify_observers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification == self.NOTE2)

        view.notify_observers(Notification(self.NOTE3))
        self.assertEqual(True, self.lastNotification == self.NOTE3)

        view.remove_mediator(utils.view.ViewTestMediator2.NAME)

        self.assertEqual(True, view.retrieve_mediator(utils.view.ViewTestMediator2.NAME) is None)

        self.lastNotification = None

        view.notify_observers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification != self.NOTE1)

        view.notify_observers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification != self.NOTE2)

        view.notify_observers(Notification(self.NOTE3))
        self.assertEqual(True, self.lastNotification == self.NOTE3)

        self.__cleanup()

    def testMediatorReregistration(self):
        """
        Tests registering the same mediator twice.
        A subsequent notification should only illicit
        one response. Also, since reregistration
        was causing 2 observers to be created, ensure
        that after removal of the mediator there will
        be no further response.

        Added for the fix deployed in version 2.0.4
        """

        view = View('test')

        view.register_mediator(utils.view.ViewTestMediator5(self))

        # try to register another instance of that mediator (uses the same NAME constant).
        view.register_mediator(utils.view.ViewTestMediator5(self))

        self.counter = 0
        view.notify_observers(Notification(self.NOTE5))
        self.assertEqual(1, self.counter)

        view.remove_mediator(utils.view.ViewTestMediator5.NAME)

        self.assertEqual(True, view.retrieve_mediator(utils.view.ViewTestMediator5.NAME ) is None)

        self.counter=0
        view.notify_observers(Notification(self.NOTE5))
        self.assertEqual(0,  self.counter)

    def testRemoveSelf(self):
        view = View('test')
        view.register_mediator(utils.view.ViewTestMediator2(self))
        view.register_mediator(utils.view.ViewTestMediator3(self))

        self.assertTrue(self.NOTE5 in view.observer_map)
        view.notify_observers(Notification(self.NOTE5))
        self.assertFalse(self.NOTE5 in view.observer_map)
