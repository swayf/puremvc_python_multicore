"""
 PureMVC Multicore Port, pep8 by Oleg Butovich <obutovich@gmail.com>
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""
from puremvc_multicore.interfaces import IMediator, INotifier
from puremvc_multicore.patterns.notifier import Notifier


class Mediator(Notifier, IMediator, INotifier):
    """
    A base C{IMediator} implementation.

    @see: L{View<org.puremvc_multicore.as3.core.view.View>}
    """

    NAME = None
    view_component = None
    mediator_name = None

    def __init__(self, mediator_name=None, view_component=None):
        """
        Mediator Constructor

        Typically, a C{Mediator} will be written to serve
        one specific control or group controls and so,
        will not have a need to be dynamically named.
        """
        self.__class__.NAME = self.__class__.NAME or self.__class__.__name__
        mediator_name = mediator_name or self.NAME
        if mediator_name is None:
            raise ValueError("Mediator name cannot be None")
        self.mediator_name = mediator_name
        self.view_component = view_component


    def get_mediator_name(self):
        """
        Get the name of the C{Mediator}.
        @return: the Mediator name
        """
        return self.mediator_name


    def set_view_component(self,view_component):
        """
        Set the C{IMediator}'s view component.

        @param view_component: the view component
        """
        self.view_component = view_component


    def get_view_component(self):
        """
        Get the C{Mediator}'s view component.

        @return: the view component
        """
        return self.view_component


    def list_notification_interests(self):
        """
        List the C{INotification} names this
        C{Mediator} is interested in being notified of.

        @return: List the list of C{INotification} names
        """
        return []


    def handle_notification(self,notification):
        """
        Handle C{INotification}s.

        Typically this will be handled in a if/else statement,
        with one 'comparison' entry per C{INotification}
        the C{Mediator} is interested in.
        """
        pass


    def on_register(self):
        """
        Called by the View when the Mediator is registered
        """
        pass


    def on_remove(self):
        """
        Called by the View when the Mediator is removed
        """
        pass
