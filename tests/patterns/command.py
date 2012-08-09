from nose.tools import eq_
from puremvc_multicore.patterns.command import SimpleCommand
from puremvc_multicore.patterns.facade import Facade
from puremvc_multicore.patterns.mediator import Mediator
import puremvc_multicore.patterns.observer
import utils.command

def testMacroCommandExecute():
    """CommandTest: Test MacroCommand execute()"""
    vo = utils.command.MacroCommandTestVO(5)
    note = puremvc_multicore.patterns.observer.Notification('MacroCommandTest', vo)
    command = utils.command.MacroCommandTestCommand()
    command.execute(note)
    eq_(vo.result1, 10)
    eq_(vo.result2, 25)


def testSimpleCommandExecute():
    """CommandTest: Test SimpleCommand execute()"""
    vo = utils.command.SimpleCommandTestVO(5)
    note = puremvc_multicore.patterns.observer.Notification('SimpleCommandTestNote', vo)
    command = utils.command.SimpleCommandTestCommand()
    command.execute(note)
    eq_(vo.result, 10)


class TestCommand(SimpleCommand):
    def execute(self, note):
        self.facade.send_notification('TEST_NOTIFICATION')

class TestMediator(Mediator):
    _test_var = None
    def list_notification_interests(self):
        return ['TEST_NOTIFICATION']

    def handle_notification(self, note):
        if note.get_name() == 'TEST_NOTIFICATION':
           self._test_var = 10


def test_command_send_notification():
    facade = Facade('test_command_send_notification')
    facade.register_command('COMMAND', TestCommand)
    facade.register_mediator(TestMediator())

    facade.send_notification('COMMAND')
    eq_(facade.retrieve_mediator('TestMediator')._test_var, 10)