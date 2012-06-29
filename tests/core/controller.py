import unittest
from puremvc_multicore.core import Controller
from puremvc_multicore.interfaces import IController
from puremvc_multicore.patterns.observer import Notification
import utils.controller


class ControllerTest(unittest.TestCase):
    """ControllerTest: Test Controller Singleton"""
    def assertNotNone(self):
        """ControllerTest: Test instance not null"""
        controller = Controller('test')
        self.assertNotEqual(None, controller)

    def assertIController(self):
        """ControllerTest: Test instance implements IController"""
        controller = Controller('test')
        self.assertEqual(True, isinstance(controller, IController))

    def testRegisterAndExecuteCommand(self):
        """ControllerTest: Test registerCommand() and executeCommand()"""
        controller = Controller('test')
        controller.registerCommand('ControllerTest', utils.controller.ControllerTestCommand)

        vo = utils.controller.ControllerTestVO(12)
        note = Notification('ControllerTest', vo)

        controller.executeCommand(note)

        self.assertEqual(True, vo.result == 24 )

    def testRegisterAndRemoveCommand(self):
        """ControllerTest: Test registerCommand() and removeCommand()"""
        controller = Controller('test')
        controller.registerCommand('ControllerRemoveTest', utils.controller.ControllerTestCommand)

        vo = utils.controller.ControllerTestVO(12)
        note = Notification('ControllerRemoveTest', vo)

        controller.executeCommand(note)

        self.assertEqual(True, vo.result == 24 )

        vo.result = 0

        controller.removeCommand('ControllerRemoveTest')
        controller.executeCommand(note)

        self.assertEqual(True, vo.result == 0)

    def testHasCommand(self):
        """ControllerTest: Test hasCommand()"""

        controller = Controller('test')
        controller.registerCommand('hasCommandTest', utils.controller.ControllerTestCommand)

        self.assertEqual(True, controller.hasCommand('hasCommandTest'))

        controller.removeCommand('hasCommandTest')

        self.assertEqual(False, controller.hasCommand('hasCommandTest'))
