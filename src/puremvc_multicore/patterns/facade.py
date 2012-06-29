"""
 PureMVC Multicore Port, pep8 by Oleg Butovich <obutovich@gmail.com>
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""
from abc import ABCMeta
from puremvc_multicore.core import Controller, View, Model
from puremvc_multicore.interfaces import IFacade
from puremvc_multicore.patterns.observer import Notification


class FacadeMeta(ABCMeta):
    def __init__(cls, name, bases, dict):
        super(FacadeMeta, cls).__init__(name, bases, dict)
        IFacade.instance_map = {}


    def __call__(cls, key, *args,**kw):
        if key not in IFacade.instance_map:
#            if cls.__name__ == 'Facade':
#                raise RuntimeError('Cannot create instances of Facade directly.')
            IFacade.instance_map[key] = super(FacadeMeta, cls).__call__(key, *args, **kw)
        return IFacade.instance_map[key]



class Facade(IFacade):
    """
    A base Singleton C{IFacade} implementation.

    In PureMVC, the C{Facade} class assumes these
    responsibilities:

    Initializing the C{Model}, C{View} and C{Controller} Singletons.

    Providing all the methods defined by the C{IModel, IView, & IController} interfaces.

    Providing the ability to override the specific C{Model}, C{View} and C{Controller} Singletons created.

    Providing a single point of contact to the application for registering C{Commands} and notifying C{Observers}


    @see: L{Model<org.puremvc_multicore.as3.core.model.Model>}
    @see: L{View<org.puremvc_multicore.as3.core.view.View>}
    @see: L{Controller<org.puremvc_multicore.as3.core.controller.Controller>}
    @see: L{Notification<org.puremvc_multicore.as3.patterns.observer.Notification>}
    @see: L{Mediator<org.puremvc_multicore.as3.patterns.mediator.Mediator>}
    @see: L{Proxy<org.puremvc_multicore.as3.patterns.proxy.Proxy>}
    @see: L{SimpleCommand<org.puremvc_multicore.as3.patterns.command.SimpleCommand>}
    @see: L{MacroCommand<org.puremvc_multicore.as3.patterns.command.MacroCommand>}
    """

    __metaclass__ = FacadeMeta

    controller = None
    model = None
    view = None


    def __init__(self, key):
        """
        Initialize the Singleton C{Facade} instance.

        Called automatically by the constructor. Override in your
        subclass to do any subclass specific initializations. Be
        sure to call C{Facade.initializeFacade()}, though.
        """
        self.initialize_notifier(key)
        self.initialize_controller()
        self.initialize_model()
        self.initialize_view()


    def initialize_controller(self):
        """
        Initialize the C{Controller}.

        Called by the C{initializeFacade} method.
        Override this method in your subclass of C{Facade}
        if one or both of the following are true:

        You wish to initialize a different C{IController}.
        You have C{Commands} to register with the C{Controller} at startup.

        If you don't want to initialize a different C{IController},
        call C{super.initialize_controller()} at the beginning of your method, then register C{Proxy}s.

        Note: This method is I{rarely} overridden; in practice you are more
        likely to use a C{Command} to create and register C{Proxy}s
        with the C{Model}, since C{Proxy}s with mutable data will likely
        need to send C{INotification}s and thus will likely want to fetch a reference to
        the C{Facade} during their construction.
        """
        if self.controller is None:
            self.controller = Controller(self.multiton_key)


    def initialize_model(self):
        """
        Initialize the C{Model}.

        Called by the C{initializeFacade} method.
        Override this method in your subclass of C{Facade}
        if one or both of the following are true:

        You wish to initialize a different C{IModel}.

        You have C{Proxy}s to register with the Model that do not
        retrieve a reference to the Facade at construction time.

        If you don't want to initialize a different C{IModel},
        call C{super.initialize_model()} at the beginning of your
        method, then register C{Proxy}s.

        Note: This method is I{rarely} overridden; in practice you are more
        likely to use a C{Command} to create and register C{Proxy}s
        with the C{Model}, since C{Proxy}s with mutable data will likely
        need to send C{INotification}s and thus will likely want to fetch a reference to
        the C{Facade} during their construction.
        """
        if self.model is None:
            self.model = Model(self.multiton_key)


    def initialize_view(self):
        """
        Initialize the C{View}.


        Called by the C{initializeFacade} method.
        Override this method in your subclass of C{Facade}
        if one or both of the following are true:

        You wish to initialize a different C{IView}.

        You have C{Observers} to register with the C{View}

        If you don't want to initialize a different C{IView},
        call C{super.initialize_view()} at the beginning of your
        method, then register C{IMediator} instances.

        Note: This method is I{rarely} overridden; in practice you are more
        likely to use a C{Command} to create and register C{Mediator}s
        with the C{View}, since C{IMediator} instances will need to send
        C{INotification}s and thus will likely want to fetch a reference
        to the C{Facade} during their construction.
        """
        if self.view is  None:
            self.view = View(self.multiton_key)


    def register_command(self, notificationName, command_class_ref):
        """
        Register an C{ICommand} with the C{Controller} by Notification name.

        @param notificationName: the name of the C{INotification} to associate the C{ICommand} with
        @param command_class_ref: a reference to the Class of the C{ICommand}
        """
        self.controller.register_command(notificationName, command_class_ref)


    def remove_command(self, notification_name):
        """
        Remove a previously registered C{ICommand} to C{INotification} mapping from the Controller.

        @param notification_name: the name of the C{INotification} to remove the C{ICommand} mapping for
        """
        self.controller.remove_command(notification_name)


    def has_command(self, notification_name):
        """
        Check if a Command is registered for a given Notification

        @param notification_name: the name of the C{INotification}
        @return: whether a Command is currently registered for the given C{notification_name}.
        """
        return self.controller.has_command(notification_name)


    def register_proxy(self, proxy):
        """
        Register an C{IProxy} with the C{Model} by name.

        @param proxy: the C{IProxy} instance to be registered with the C{Model}.
        """
        self.model.register_proxy(proxy)


    def retrieve_proxy(self, proxy_name):
        """
        Retrieve an C{IProxy} from the C{Model} by name.

        @param proxy_name: the name of the proxy to be retrieved.
        @return: the C{IProxy} instance previously registered with the given C{proxy_name}.
        """
        return self.model.retrieve_proxy(proxy_name)


    def remove_proxy(self, proxy_name):
        """
        Remove an C{IProxy} from the C{Model} by name.

        @param proxy_name: the C{IProxy} to remove from the C{Model}.
        @return: the C{IProxy} that was removed from the C{Model}
        """
        proxy = None
        if self.model is not None:
            proxy = self.model.remove_proxy(proxy_name)
        return proxy


    def has_proxy(self, proxy_name):
        """
        Check if a Proxy is registered

        @param proxy_name: the name of the C{IProxy}
        @return: whether a Proxy is currently registered with the given C{proxy_name}.
        """
        return self.model.has_proxy(proxy_name)


    def register_mediator(self, mediator):
        """
        Register a C{IMediator} with the C{View}.

        @param mediator: a reference to the C{IMediator}
        """
        if self.view is not None:
            self.view.register_mediator(mediator)


    def retrieve_mediator(self, mediator_name):
        """
        Retrieve an C{IMediator} from the C{View}.

        @param mediator_name: the name of the C{IMediator}
        @return: the C{IMediator} previously registered with the given C{mediator_name}.
        """
        return self.view.retrieve_mediator(mediator_name)


    def remove_mediator(self, mediator_name):
        """
        Remove an C{IMediator} from the C{View}.

        @param mediator_name: name of the C{IMediator} to be removed.
        @return: the C{IMediator} that was removed from the C{View}
        """
        mediator = None
        if self.view is not None:
            mediator = self.view.remove_mediator(mediator_name)
        return mediator


    def has_mediator(self, mediator_name):
        """
        Check if a Mediator is registered or not

        @param mediator_name: the name of the C{IMediator}
        @return: whether a Mediator is registered with the given C{mediator_name}.
        """
        return self.view.has_mediator(mediator_name)


    def send_notification(self, notification_name, body=None, type=None):
        """
        Create and send an C{INotification}.

        Keeps us from having to construct new notification
        instances in our implementation code.

        @param notification_name: the name of the notification to send
        @param body: the body of the notification (optional)
        @param type: the type of the notification (optional)
        """
        self.notify_observers(Notification(notification_name, body, type))


    def notify_observers(self, notification):
        """
        Notify C{Observer}s.

        This method is left public mostly for backward
        compatibility, and to allow you to send custom
        notification classes using the facade.

        Usually you should just call send_notification
        and pass the parameters, never having to
        construct the notification yourself.

        @param notification: the C{INotification} to have the C{View} notify C{Observers} of.
        """
        if self.view is not None:
            self.view.notify_observers(notification)


    def initialize_notifier(self, key):
        self.multiton_key = key

