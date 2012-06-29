from puremvc_multicore.interfaces import INotification, IMediator
from puremvc_multicore.patterns.mediator import Mediator
from puremvc_multicore.patterns.observer import Notification

class ViewTestNote(Notification, INotification):

    NAME = "ViewTestNote"

    def __init__(self, anme, body):
        Notification.__init__(self, ViewTestNote.NAME, body)

    @staticmethod
    def create(body):
        return ViewTestNote(ViewTestNote.NAME, body)

class ViewTestMediator(Mediator, IMediator):

    NAME = 'ViewTestMediator'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator.NAME, view)

    def list_notification_interests(self):
        return ['ABC', 'DEF', 'GHI']

class ViewTestMediator2(Mediator, IMediator):

    NAME = 'ViewTestMediator2'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator2.NAME, view)

    def list_notification_interests(self):
        return [
            self.view_component.NOTE1,
            self.view_component.NOTE2,
            self.view_component.NOTE5,
        ]

    def handle_notification(self, notification):
        self.view_component.lastNotification = notification.get_name()
        if notification.get_name() == self.view_component.NOTE5:
            self.facade.remove_mediator(self.NAME)

class ViewTestMediator3(Mediator, IMediator):

    NAME = 'ViewTestMediator3'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator3.NAME, view)

    def list_notification_interests(self):
        return [
            self.view_component.NOTE3,
            self.view_component.NOTE5,
        ]

    def handle_notification(self, notification):
        self.view_component.lastNotification = notification.get_name()
        if notification.get_name() == self.view_component.NOTE5:
            self.facade.remove_mediator(self.NAME)

class ViewTestMediator4(Mediator, IMediator):

    NAME = 'ViewTestMediator4'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator4.NAME, view)

    def on_register(self):
        self.view_component.onRegisterCalled = True

    def on_remove(self):
        self.view_component.onRemoveCalled = True

class ViewTestMediator5(Mediator, IMediator):

    NAME = 'ViewTestMediator5'

    def __init__(self, view):
        Mediator.__init__(self, ViewTestMediator5.NAME, view)

    def list_notification_interests(self):
        return [self.view_component.NOTE5]

    def handle_notification(self, notification):
        self.view_component.counter += 1
