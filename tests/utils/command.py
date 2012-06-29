from puremvc_multicore.patterns.command import SimpleCommand, MacroCommand

class MacroCommandTestCommand(MacroCommand):
    def initialize_macro_command(self):
        self.add_sub_command(MacroCommandTestSub1Command)
        self.add_sub_command(MacroCommandTestSub2Command)

class MacroCommandTestSub1Command(SimpleCommand):
    def execute(self,note):
        vo = note.get_body()
        vo.result1 = 2 * vo.input

class MacroCommandTestSub2Command(SimpleCommand):
    def execute(self,note):
        vo = note.get_body()
        vo.result2 = vo.input * vo.input

class MacroCommandTestVO(object):

    input = None
    result1 = None
    result2 = None

    def __init__(self, input):
        self.input = input

class SimpleCommandTestCommand(SimpleCommand):
    def execute(self,note):
        vo = note.get_body()
        vo.result = 2 * vo.input

class SimpleCommandTestVO(object):

    input = None
    result = None

    def __init__(self, input):
        self.input = input
