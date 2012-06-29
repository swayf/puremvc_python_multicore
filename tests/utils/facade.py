from puremvc_multicore.patterns.command import SimpleCommand

class FacadeTestCommand(SimpleCommand):
    def execute(self,note):
        vo = note.get_body()
        vo.result = 2 * vo.input

class FacadeTestVO(object):

    input = None
    result = None

    def __init__(self,input):
        self.input = input
