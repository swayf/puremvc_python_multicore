import puremvc.patterns.observer
import puremvc.interfaces
import puremvc.patterns.mediator

class ViewTestNote(puremvc.patterns.observer.Notification, puremvc.interfaces.INotification):

    NAME = "ViewTestNote"

    def __init__(self, anme, body):
        puremvc.patterns.observer.Notification.__init__(self, ViewTestNote.NAME, body)

    @staticmethod
    def create(body):
        return ViewTestNote(ViewTestNote.NAME, body)

class ViewTestMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):

    NAME = 'ViewTestMediator'

    def __init__(self, view):
        puremvc.patterns.mediator.Mediator.__init__(self, ViewTestMediator.NAME, view)

    def listNotificationInterests(self):
        return ['ABC', 'DEF', 'GHI']

class ViewTestMediator2(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):

    NAME = 'ViewTestMediator2'

    def __init__(self, view):
        puremvc.patterns.mediator.Mediator.__init__(self, ViewTestMediator2.NAME, view)

    def listNotificationInterests(self):
        return [
            self.view_component.NOTE1,
            self.view_component.NOTE2,
            self.view_component.NOTE5,
        ]

    def handleNotification(self, notification):
        self.view_component.lastNotification = notification.getName()
        if notification.getName() == self.view_component.NOTE5:
            self.facade.removeMediator(self.NAME)

class ViewTestMediator3(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):

    NAME = 'ViewTestMediator3'

    def __init__(self, view):
        puremvc.patterns.mediator.Mediator.__init__(self, ViewTestMediator3.NAME, view)

    def listNotificationInterests(self):
        return [
            self.view_component.NOTE3,
            self.view_component.NOTE5,
        ]

    def handleNotification(self, notification):
        self.view_component.lastNotification = notification.getName()
        if notification.getName() == self.view_component.NOTE5:
            self.facade.removeMediator(self.NAME)

class ViewTestMediator4(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):

    NAME = 'ViewTestMediator4'

    def __init__(self, view):
        puremvc.patterns.mediator.Mediator.__init__(self, ViewTestMediator4.NAME, view)

    def onRegister(self):
        self.view_component.onRegisterCalled = True

    def onRemove(self):
        self.view_component.onRemoveCalled = True

class ViewTestMediator5(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):

    NAME = 'ViewTestMediator5'

    def __init__(self, view):
        puremvc.patterns.mediator.Mediator.__init__(self, ViewTestMediator5.NAME, view)

    def listNotificationInterests(self):
        return [self.view_component.NOTE5]

    def handleNotification(self, notification):
        self.view_component.counter += 1
