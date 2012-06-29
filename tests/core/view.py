import unittest
import utils.view
from puremvc.core import View
from puremvc.interfaces import IView
from puremvc.patterns.mediator import Mediator
from puremvc.patterns.observer import Observer, Notification


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
        View('test').removeMediator(utils.view.ViewTestMediator.NAME)
        View('test').removeMediator(utils.view.ViewTestMediator2.NAME)
        View('test').removeMediator(utils.view.ViewTestMediator3.NAME)
        View('test').removeMediator(utils.view.ViewTestMediator4.NAME)
        View('test').removeMediator(utils.view.ViewTestMediator5.NAME)

    def assertNotNone(self):
        """ViewTest: Test instance not null"""
        view = View('test')
        self.assertNotEqual(None, view)

    def assertIView(self):
        """ViewTest: Test instance implements IView"""
        view = View('test')
        self.assertEqual(True, isinstance(view, IView))

    def testRegisterAndNotifyObserver(self):
        """ViewTest: Test registerObserver() and notifyObservers()"""

        self.viewTestVar = 0
        def viewTestMethod(note):
            self.viewTestVar = note.getBody()

        view = View('test')
        obsvr = Observer(viewTestMethod, self)
        view.registerObserver(utils.view.ViewTestNote.NAME, obsvr)

        note = utils.view.ViewTestNote.create(10)
        view.notifyObservers(note)

        self.assertEqual(True, self.viewTestVar == 10)

    def testRegisterAndRetrieveMediator(self):
        """ViewTest: Test registerMediator() and retrieveMediator()"""
        view = View('test')

        viewTestMediator = utils.view.ViewTestMediator(self)
        view.registerMediator(viewTestMediator)

        mediator = view.retrieveMediator(utils.view.ViewTestMediator.NAME)

        self.assertEqual(True, isinstance(mediator, utils.view.ViewTestMediator))
        self.__cleanup()

    def testHasMediator(self):
        """ViewTest: Test hasMediator()"""
        view = View('test')
        meditr = Mediator('hasMediatorTest', self)
        view.registerMediator(meditr)

        self.assertEqual(True, view.hasMediator('hasMediatorTest'))

        view.removeMediator('hasMediatorTest')

        self.assertEqual(False, view.hasMediator('hasMediatorTest'))
        self.__cleanup()

    def testRegisterAndRemoveMediator(self):
        """ViewTest: Test registerMediator() and removeMediator()"""
        view = View('test')

        meditr = Mediator('testing', self)
        view.registerMediator(meditr)

        removedMediator = view.removeMediator('testing')

        self.assertEqual(True, removedMediator.getMediatorName() == 'testing')

        self.assertEqual(True, view.retrieveMediator('testing') is None)
        self.__cleanup()

    def testOnRegisterAndOnRemove(self):
        """ViewTest: Test onRegsiter() and onRemove()"""
        view = View('test')

        mediator = utils.view.ViewTestMediator4(self)
        view.registerMediator(mediator)

        self.assertEqual(True, self.onRegisterCalled)

        view.removeMediator(utils.view.ViewTestMediator4.NAME)

        self.assertEqual(True, self.onRemoveCalled)
        self.__cleanup()


    def testSuccessiveRegisterAndRemoveMediator(self):
        """ViewTest: Test Successive registerMediator() and removeMediator()"""
        view = View('test')

        view.registerMediator(utils.view.ViewTestMediator(self))

        self.assertEqual(True, isinstance(view.retrieveMediator(utils.view.ViewTestMediator.NAME), utils.view.ViewTestMediator))

        view.removeMediator(utils.view.ViewTestMediator.NAME)

        self.assertEqual(True, view.retrieveMediator(utils.view.ViewTestMediator.NAME) is None)

        self.assertEqual(True, view.removeMediator(utils.view.ViewTestMediator.NAME) is None)

        view.registerMediator(utils.view.ViewTestMediator(self))

        self.assertEqual(True, isinstance(view.retrieveMediator(utils.view.ViewTestMediator.NAME), utils.view.ViewTestMediator))

        view.removeMediator(utils.view.ViewTestMediator.NAME)

        self.assertEqual(True, view.retrieveMediator(utils.view.ViewTestMediator.NAME) is None)

        self.__cleanup()

    def testRemoveMediatorAndSubsequentNotify(self):
        """ViewTest: Test removeMediator() and subsequent nofity()"""

        view = View('test')

        view.registerMediator(utils.view.ViewTestMediator2(self))

        view.notifyObservers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification == self.NOTE1)

        view.notifyObservers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification == self.NOTE2)

        view.removeMediator(utils.view.ViewTestMediator2.NAME)

        self.assertEqual(True, view.retrieveMediator(utils.view.ViewTestMediator2.NAME) is None)

        self.lastNotification = None

        view.notifyObservers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification != self.NOTE1)

        view.notifyObservers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification != self.NOTE2)

        self.__cleanup()

    def testRemoveOneOfTwoMediatorsAndSubsequentNotify(self):
        """ViewTest: Test removing one of two Mediators and subsequent notify()"""

        view = View('test')

        view.registerMediator(utils.view.ViewTestMediator2(self))

        view.registerMediator(utils.view.ViewTestMediator3(self))

        view.notifyObservers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification == self.NOTE1)

        view.notifyObservers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification == self.NOTE2)

        view.notifyObservers(Notification(self.NOTE3))
        self.assertEqual(True, self.lastNotification == self.NOTE3)

        view.removeMediator(utils.view.ViewTestMediator2.NAME)

        self.assertEqual(True, view.retrieveMediator(utils.view.ViewTestMediator2.NAME) is None)

        self.lastNotification = None

        view.notifyObservers(Notification(self.NOTE1))
        self.assertEqual(True, self.lastNotification != self.NOTE1)

        view.notifyObservers(Notification(self.NOTE2))
        self.assertEqual(True, self.lastNotification != self.NOTE2)

        view.notifyObservers(Notification(self.NOTE3))
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

        view.registerMediator(utils.view.ViewTestMediator5(self))

        # try to register another instance of that mediator (uses the same NAME constant).
        view.registerMediator(utils.view.ViewTestMediator5(self))

        self.counter = 0
        view.notifyObservers(Notification(self.NOTE5))
        self.assertEqual(1, self.counter)

        view.removeMediator(utils.view.ViewTestMediator5.NAME)

        self.assertEqual(True, view.retrieveMediator(utils.view.ViewTestMediator5.NAME ) is None)

        self.counter=0
        view.notifyObservers(Notification(self.NOTE5))
        self.assertEqual(0,  self.counter)

    def testRemoveSelf(self):
        view = View('test')
        view.registerMediator(utils.view.ViewTestMediator2(self))
        view.registerMediator(utils.view.ViewTestMediator3(self))

        self.assertTrue(self.NOTE5 in view.observer_map)
        view.notifyObservers(Notification(self.NOTE5))
        self.assertFalse(self.NOTE5 in view.observer_map)
