from puremvc_multicore.patterns.proxy import Proxy

class ModelTestProxy(Proxy):
    NAME = 'ModelTestProxy'
    ON_REGISTER_CALLED = 'on_register Called'
    ON_REMOVE_CALLED = 'on_remove Called'

    def __init__(self):
        Proxy.__init__(self, ModelTestProxy.NAME, object())

    def on_register(self):
        self.set_data(ModelTestProxy.ON_REGISTER_CALLED)

    def on_remove(self):
        self.set_data(ModelTestProxy.ON_REMOVE_CALLED)
