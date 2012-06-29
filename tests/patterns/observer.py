import unittest
from puremvc_multicore.patterns.observer import Observer, Notification

class ObserverTest(unittest.TestCase):
    """ObserverTest: Test Observer Pattern"""

    __observerTestVar = None

    def __observerTestMethod(self,note):
        self.__observerTestVar = note.getBody()

    def testObserverAccessors(self):
        """ObserverTest: Test Observer Accessors"""

        obsrvr = Observer(None,None)
        obsrvr.setNotifyContext(self)

        obsrvr.setNotifyMethod(self.__observerTestMethod)

        note = Notification('ObserverTestNote',10)
        obsrvr.notifyObserver(note)

        self.assertEqual(True, self.__observerTestVar == 10)

    def testObserverConstructor(self):
        """ObserverTest: Test Observer Constructor"""

        obsrvr = Observer(self.__observerTestMethod,self)

        note = Notification('ObserverTestNote',5)
        obsrvr.notifyObserver(note)

        self.assertEqual(True, self.__observerTestVar == 5)

    def testCompareNotifyContext(self):
        """ObserverTest: Test compareNotifyContext()"""

        obsrvr = Observer(self.__observerTestMethod, self)

        negTestObj = object()

        self.assertEqual(False, obsrvr.compareNotifyContext(negTestObj))
        self.assertEqual(True, obsrvr.compareNotifyContext(self))

    def testNameAccessors(self):
        """NotificationTest: Test Name Accessors"""

        note = Notification('TestNote')

        self.assertEqual(True, note.getName() == 'TestNote')

    def testBodyAccessors(self):
        """NotificationTest: Test Body Accessors"""

        note = Notification(None)
        note.setBody(5)

        self.assertEqual(True, note.getBody() == 5)

    def testConstructor(self):
        """NotificationTest: Test Constructor"""

        note = Notification('TestNote',5,'TestNoteType')

        self.assertEqual(True, note.getName() == 'TestNote')
        self.assertEqual(True, note.getBody() == 5)
        self.assertEqual(True, note.getType() == 'TestNoteType')
