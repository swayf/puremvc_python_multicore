"""
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""

from puremvc_multicore.interfaces import INotifier
from puremvc_multicore.patterns.facade import Facade


class Notifier(INotifier):
    """
    A Base C{INotifier} implementation.

    C{MacroCommand, Command, Mediator} and C{Proxy}
    all have a need to send C{Notifications}.

    The C{INotifier} interface provides a common method called
    C{sendNotification} that relieves implementation code of
    the necessity to actually construct C{Notifications}.

    The C{Notifier} class, which all of the above mentioned classes
    extend, provides an initialized reference to the C{Facade}
    Singleton, which is required for the convenience method
    for sending C{Notifications}, but also eases implementation as these
    classes have frequent C{Facade} interactions and usually require
    access to the facade anyway.

    @see: L{Facade<org.puremvc_multicore.as3.patterns.facade.Facade>}
    @see: L{Mediator<org.puremvc_multicore.as3.patterns.mediator.Mediator>}
    @see: L{Proxy<org.puremvc_multicore.as3.patterns.proxy.Proxy>}
    @see: L{SimpleCommand<org.puremvc_multicore.as3.patterns.command.SimpleCommand>}
    @see: L{MacroCommand<org.puremvc_multicore.as3.patterns.command.MacroCommand>}
    """
    multiton_key = None

    @property
    def facade(self):
        if self.multiton_key is None:
            raise RuntimeError("multitonKey for this Notifier not yet initialized!")
        return Facade(self.multiton_key)


    def sendNotification(self, notificationName, body=None, type=None):
        """
        Create and send an C{INotification}.

        Keeps us from having to construct new INotification
        instances in our implementation code.

        @param notificationName: the name of the notification to send
        @param body: the body of the notification (optional)
        @param type: the type of the notification (optional)
        """
        self.facade.sendNotification(notificationName, body, type)


    def initializeNotifier(self, key):
        self.multiton_key = key

