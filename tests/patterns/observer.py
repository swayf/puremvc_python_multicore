from nose.tools import eq_, ok_
from puremvc_multicore.patterns.observer import Observer, Notification


class ObserverTester(object):
    observerTestVar = None
    def observerTestMethod(self, note):
       self.observerTestVar = note.get_body()


def testObserverAccessors():
    """ObserverTest: Test Observer Accessors"""
    observer = Observer(None,None)
    tester = ObserverTester()
    observer.set_notify_method(tester.observerTestMethod)
    observer.set_notify_context(tester)

    note = Notification('ObserverTestNote',10)
    observer.notify_observer(note)

    eq_(tester.observerTestVar, 10)


def testObserverConstructor():
    """ObserverTest: Test Observer Constructor"""
    tester = ObserverTester()
    observer = Observer(tester.observerTestMethod, tester)

    note = Notification('ObserverTestNote',5)
    observer.notify_observer(note)

    eq_(tester.observerTestVar, 5)


def testCompareNotifyContext():
    """ObserverTest: Test compare_notify_context()"""
    tester = ObserverTester()
    observer = Observer(tester.observerTestMethod, tester)

    ok_(not observer.compare_notify_context(object()))
    ok_(observer.compare_notify_context(tester))


def testNameAccessors():
    """NotificationTest: Test Name Accessors"""
    note = Notification('TestNote')
    eq_(note.get_name(), 'TestNote')


def testBodyAccessors():
    """NotificationTest: Test Body Accessors"""
    note = Notification(None)
    note.set_body(5)

    eq_(note.get_body(), 5)


def testConstructor():
    """NotificationTest: Test Constructor"""
    note = Notification('TestNote', 5, 'TestNoteType')

    eq_(note.get_name(), 'TestNote')
    eq_(note.get_body(), 5)
    eq_(note.get_type(), 'TestNoteType')
