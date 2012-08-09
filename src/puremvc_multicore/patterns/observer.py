"""
 PureMVC Multicore Port, pep8 by Oleg Butovich <obutovich@gmail.com>
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""

from puremvc_multicore.interfaces import IObserver, INotification

class Observer(IObserver):
    """
    A base C{IObserver} implementation.

    An C{Observer} is an object that encapsulates information
    about an interested object with a method that should
    be called when a particular C{INotification} is broadcast.

    In PureMVC, the C{Observer} class assumes these responsibilities:

    Encapsulate the notification (callback) method of the interested object.

    Encapsulate the notification context (this) of the interested object.

    Provide methods for setting the notification method and context.

    Provide a method for notifying the interested object.

    @see: L{View<org.puremvc_multicore.as3.core.view.View>}
    @see: L{Notification<org.puremvc_multicore.as3.patterns.observer.Notification>}
    """
    notify = None
    context = None

    def __init__(self, notify_method, notify_context = None):
        """
        Constructor.

        The notification method on the interested object should take
        one parameter of type C{INotification}

        @param notify_method: the notification method of the interested object
        @param notify_context: the notification context of the interested object
        """
        self.set_notify_method(notify_method)
        self.set_notify_context(notify_context)


    def set_notify_method(self, notify_method):
        """
        Set the notification method.

        The notification method should take one parameter of type C{INotification}.

        @param notify_method: the notification (callback) method of the interested object.
        """
        self.notify = notify_method


    def set_notify_context(self, notify_context):
        """
        Set the notification context.

        @param notify_context: the notification context (this) of the interested object.
        """
        self.context = notify_context


    def get_notify_method(self):
        """
        Get the notification method.

        @return: the notification (callback) method of the interested object.
        """
        return self.notify


    def get_notify_context(self):
        """
        Get the notification context.

        @return: the notification context (C{this}) of the interested object.
        """
        return self.context


    def notify_observer(self, notification):
        """
        Notify the interested object.

        @param notification: the C{INotification} to pass to the interested object's notification method.
        """
        self.get_notify_method()(notification)


    def compare_notify_context(self, obj):
        """
        Compare an object to the notification context.

        @param obj: the object to compare
        @return: boolean indicating if the object and the notification context are the same
        """
        return obj is self.context



class Notification(INotification):
    """
    A base C{INotification} implementation.

    PureMVC does not rely upon underlying event models such
    as the one provided with Flash, and ActionScript 3 does
    not have an inherent event model.</P>

    The Observer Pattern as implemented within PureMVC exists
    to support event-driven communication between the
    application and the actors of the MVC triad.</P>

    Notifications are not meant to be a replacement for Events
    in Flex/Flash/Apollo. Generally, C{IMediator} implementors
    place event listeners on their view components, which they
    then handle in the usual way. This may lead to the broadcast of C{Notification}s to
    trigger C{ICommand}s or to communicate with other C{IMediators}. C{IProxy} and C{ICommand}
    instances communicate with each other and C{IMediator}s
    by broadcasting C{INotification}s.</P>

    A key difference between Flash C{Event}s and PureMVC
    C{Notification}s is that C{Event}s follow the
    'Chain of Responsibility' pattern, 'bubbling' up the display hierarchy
    until some parent component handles the C{Event}, while
    PureMVC C{Notification}s follow a 'Publish/Subscribe'
    pattern. PureMVC classes need not be related to each other in a
    parent/child relationship in order to communicate with one another
    using C{Notification}s.

    @see: L{Observer<org.puremvc_multicore.as3.patterns.observer.Observer>}
    """

    name = None
    body = None
    type = None

    def __init__(self,  name, body=None, type=None):
        """
        Constructor.

        @param name: name of the C{Notification} instance. (required)
        @param body: the C{Notification} body. (optional)
        @param type; the type of the C{Notification} (optional)
        """
        self.name = name
        self.body = body
        self.type = type


    def get_name(self):
        """
        Get the name of the C{Notification} instance.

        @return: the name of the C{Notification} instance.
        """
        return self.name


    def set_body(self, body):
        """
        Set the body of the C{Notification} instance.
        """
        self.body = body


    def get_body(self):
        """
        Get the body of the C{Notification} instance.

        @return: the body object.
        """
        return self.body


    def set_type(self, type):
        """
        Set the type of the C{Notification} instance.
        """
        self.type = type


    def get_type(self):
        """
        Get the type of the C{Notification} instance.

        @return: the type
        """
        return self.type


    def str(self):
        """
        Get the string representation of the C{Notification} instance.

        @return: the string representation of the C{Notification} instance.
        """
        msg = "Notification Name: " + self.get_name()

        bd = "None"
        if self.body is not None:
            bd = str(self.body)

        ty = "None"
        if self.type is not None:
            ty = self.type

        msg += "\nBody:"+bd
        msg += "\nType:"+ty
        return msg
