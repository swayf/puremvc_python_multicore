from puremvc_multicore.patterns.command import SimpleCommand, MacroCommand

class MacroCommandTestCommand(MacroCommand):
    def initializeMacroCommand(self):
        self.addSubCommand(MacroCommandTestSub1Command)
        self.addSubCommand(MacroCommandTestSub2Command)

class MacroCommandTestSub1Command(SimpleCommand):
    def execute(self,note):
        vo = note.getBody()
        vo.result1 = 2 * vo.input

class MacroCommandTestSub2Command(SimpleCommand):
    def execute(self,note):
        vo = note.getBody()
        vo.result2 = vo.input * vo.input

class MacroCommandTestVO(object):

    input = None
    result1 = None
    result2 = None

    def __init__(self, input):
        self.input = input

class SimpleCommandTestCommand(SimpleCommand):
    def execute(self,note):
        vo = note.getBody()
        vo.result = 2 * vo.input

class SimpleCommandTestVO(object):

    input = None
    result = None

    def __init__(self, input):
        self.input = input
