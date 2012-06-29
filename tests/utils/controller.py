from puremvc_multicore.patterns.command import SimpleCommand

class ControllerTestCommand(SimpleCommand):

    def execute(self, note):
        vo = note.get_body()
        vo.result = 2 * vo.input

class ControllerTestVO(object):

    input = 0
    result = 0

    def __init__(self, num=0):
        self.input = num
