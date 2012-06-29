import unittest
from puremvc_multicore.patterns.observer import Observer, Notification

class ObserverTest(unittest.TestCase):
    """ObserverTest: Test Observer Pattern"""

    __observerTestVar = None

    def __observerTestMethod(self,note):
        self.__observerTestVar = note.get_body()

    def testObserverAccessors(self):
        """ObserverTest: Test Observer Accessors"""

        obsrvr = Observer(None,None)
        obsrvr.set_notify_context(self)

        obsrvr.set_notify_method(self.__observerTestMethod)

        note = Notification('ObserverTestNote',10)
        obsrvr.notify_observer(note)

        self.assertEqual(True, self.__observerTestVar == 10)

    def testObserverConstructor(self):
        """ObserverTest: Test Observer Constructor"""

        obsrvr = Observer(self.__observerTestMethod,self)

        note = Notification('ObserverTestNote',5)
        obsrvr.notify_observer(note)

        self.assertEqual(True, self.__observerTestVar == 5)

    def testCompareNotifyContext(self):
        """ObserverTest: Test compare_notify_context()"""

        obsrvr = Observer(self.__observerTestMethod, self)

        negTestObj = object()

        self.assertEqual(False, obsrvr.compare_notify_context(negTestObj))
        self.assertEqual(True, obsrvr.compare_notify_context(self))

    def testNameAccessors(self):
        """NotificationTest: Test Name Accessors"""

        note = Notification('TestNote')

        self.assertEqual(True, note.get_name() == 'TestNote')

    def testBodyAccessors(self):
        """NotificationTest: Test Body Accessors"""

        note = Notification(None)
        note.set_body(5)

        self.assertEqual(True, note.get_body() == 5)

    def testConstructor(self):
        """NotificationTest: Test Constructor"""

        note = Notification('TestNote',5,'TestNoteType')

        self.assertEqual(True, note.get_name() == 'TestNote')
        self.assertEqual(True, note.get_body() == 5)
        self.assertEqual(True, note.get_type() == 'TestNoteType')
