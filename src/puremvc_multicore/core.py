"""
 PureMVC Multicore Port, pep8 by Oleg Butovich <obutovich@gmail.com>
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""
from abc import ABCMeta
from puremvc_multicore.interfaces import IController, IModel, IView
from puremvc_multicore.patterns.observer import Observer



class ControllerMeta(ABCMeta):
    def __init__(cls, name, bases, dict):
        super(ControllerMeta, cls).__init__(name, bases, dict)
        IController.instance_map = {}


    def __call__(cls, key, *args,**kw):
        if key not in IController.instance_map:
            IController.instance_map[key] = super(ControllerMeta, cls).__call__(key, *args, **kw)
        return IController.instance_map[key]



class Controller(IController):
    """
    A Singleton C{IController} implementation.

    In PureMVC, the C{Controller} class follows the
    'Command and Controller' strategy, and assumes these
    responsibilities:

    Remembering which C{ICommand}s
    are intended to handle which C{INotifications}.

    Registering itself as an C{IObserver} with
    the C{View} for each C{INotification}
    that it has an C{ICommand} mapping for.

    Creating a new instance of the proper C{ICommand}
    to handle a given C{INotification} when notified by the C{View}.

    Calling the C{ICommand}'s C{execute}
    method, passing in the C{INotification}.

    Your application must register C{ICommands} with the
    Controller.

    The simplest way is to subclass C{Facade},
    and use its C{initialize_controller} method to add your
    registrations.

    @see: L{View<puremvc_multicore.core.view.View>}
    @see: L{Observer<puremvc_multicore.patterns.observer.Observer>}
    @see: L{Notification<puremvc_multicore.patterns.observer.Notification>}
    @see: L{SimpleCommand<puremvc_multicore.patterns.command.SimpleCommand>}
    @see: L{MacroCommand<puremvc_multicore.patterns.command.MacroCommand>}
    """

    __metaclass__ = ControllerMeta

    view = None
    command_map = None

    def __init__(self, key):
        """
        Initialize the Singleton C{Controller} instance.

        Called automatically by the constructor.

        Note that if you are using a subclass of C{View}
        in your application, you will need to initialize the view property
        """
        self.view = View(key)
        self.command_map = {}
        self.multiton_key = key


    def execute_command(self, note):
        """
        If an C{ICommand} has previously been registered
        to handle a the given C{INotification}, then it is executed.

        @param note: an C{INotification}
        """
        command_class_ref = self.command_map.get(note.get_name(),None)
        if command_class_ref is not None:
            command_instance = command_class_ref()
            command_instance.initialize_notifier(self.multiton_key)
            command_instance.execute(note)


    def register_command(self, notification_name, command_class_ref):
        """
        Register a particular C{ICommand} class as the handler
        for a particular C{INotification}.

        If an C{ICommand} has already been registered to
        handle C{INotification}s with this name, it is no longer
        used, the new C{ICommand} is used instead.

        The Observer for the new ICommand is only created if this the
        first time an ICommand has been registered for this Notification name.

        @param notification_name: the name of the C{INotification}
        @param command_class_ref: the C{Class} of the C{ICommand}
        """
        if self.command_map.get(notification_name,None) is None:
            self.view.register_observer(notification_name, Observer(self.execute_command, self))

        self.command_map[notification_name] = command_class_ref


    def has_command(self, notification_name):
        """
        Check if a Command is registered for a given Notification

        @param notification_name: the name of the C{INotification}
        @return: whether a Command is currently registered for the given C{notification_name}.
        """
        return self.command_map.get(notification_name,None) is not None


    def remove_command(self, notification_name):
        """
        Remove a previously registered C{ICommand} to C{INotification} mapping.

        @param notification_name: the name of the C{INotification} to remove the C{ICommand} mapping for
        """
        if self.has_command(notification_name):
            self.view.remove_observer(notification_name, self)
            del self.command_map[notification_name]



class ModelMeta(ABCMeta):
    def __init__(cls, name, bases, dict):
        super(ModelMeta, cls).__init__(name, bases, dict)
        IModel.instance_map = {}


    def __call__(cls, key, *args,**kw):
        if key not in IModel.instance_map:
            IModel.instance_map[key] = super(ModelMeta, cls).__call__(key, *args, **kw)
        return IModel.instance_map[key]



class Model(IModel):
    """
    A Singleton C{IModel} implementation.

    In PureMVC, the C{Model} class provides
    access to model objects (Proxies) by named lookup.

    The C{Model} assumes these responsibilities:

    Maintain a cache of C{IProxy} instances.

    Provide methods for registering, retrieving, and removing C{IProxy} instances.

    Your application must register C{IProxy} instances
    with the C{Model}. Typically, you use an
    C{ICommand} to create and register C{IProxy}
    instances once the C{Facade} has initialized the Core
    actors.

    @see: L{Proxy<puremvc_multicore.patterns.proxy.Proxy>}
    @see: L{IProxy<puremvc_multicore.interfaces.IProxy>}
    """
    __metaclass__ = ModelMeta

    proxy_map = None


    def __init__(self, key):
        """
        Initialize the Singleton C{Model} instance.

        Called automatically by the constructor.
        """
        self.multiton_key = key
        self.proxy_map = {}


    def register_proxy(self, proxy):
        """
        Register an C{IProxy} with the C{Model}.

        @param proxy: an C{IProxy} to be held by the C{Model}.
        """
        proxy.initialize_notifier(self.multiton_key)
        self.proxy_map[proxy.get_proxy_name()] = proxy
        proxy.on_register()


    def retrieve_proxy(self, proxy_name):
        """
        Retrieve an C{IProxy} from the C{Model}.

        @param proxy_name: the name of the C{IProxy}
        @return: the C{IProxy} instance previously registered with the given C{proxy_name}.
        """
        return self.proxy_map.get(proxy_name,None)


    def has_proxy(self, proxy_name):
        """
        Check if a Proxy is registered

        @param proxy_name: the name of the C{IProxy}
        @return: whether a Proxy is currently registered with the given C{proxy_name}.
        """
        return self.proxy_map.get(proxy_name,None) is not None


    def remove_proxy(self, proxy_name):
        """
        Remove an C{IProxy} from the C{Model}.

        @param proxy_name: name of the C{IProxy} instance to be removed.
        @return: the C{IProxy} that was removed from the C{Model}
        """
        proxy = self.proxy_map.get(proxy_name,None)
        if proxy:
            del self.proxy_map[proxy_name]
            proxy.on_remove()
        return proxy



class ViewMeta(ABCMeta):
    def __init__(cls, name, bases, dict):
        super(ViewMeta, cls).__init__(name, bases, dict)
        IView.instance_map = {}


    def __call__(cls, key, *args,**kw):
        if key not in IView.instance_map:
            IView.instance_map[key] = super(ViewMeta, cls).__call__(key, *args, **kw)
        return IView.instance_map[key]


class View(IView):
    """
    A Singleton C{IView} implementation.

    In PureMVC, the C{View} class assumes these responsibilities:

    Maintain a cache of C{IMediator} instances.

    Provide methods for registering, retrieving, and removing C{IMediators}.

    Notifiying C{IMediators} when they are registered or removed.

    Managing the observer lists for each C{INotification} in the application.

    Providing a method for attaching C{IObservers} to an C{INotification}'s observer list.

    Providing a method for broadcasting an C{INotification}.

    Notifying the C{IObservers} of a given C{INotification} when it broadcast.


    @see: L{Mediator<puremvc_multicore.patterns.mediator.Mediator>}
    @see: L{Observer<puremvc_multicore.patterns.observer.Observer>}
    @see: L{Notification<puremvc_multicore.patterns.observer.Notification>}
    """
    __metaclass__ = ViewMeta

    observer_map = None
    mediator_map = None

    def __init__(self, key):
        """
        Initialize the Singleton C{View} instance.

        Called automatically by the constructor.
        """
        self.multiton_key = key
        self.observer_map = {}
        self.mediator_map = {}


    def register_observer(self, notification_name, observer):
        """
        Register an C{IObserver} to be notified
        of C{INotifications} with a given name.

        @param notification_name: the name of the C{INotifications} to notify this C{IObserver} of
        @param observer: the C{IObserver} to register
        """
        if not notification_name in self.observer_map:
            self.observer_map[notification_name] = []
        self.observer_map[notification_name].append(observer)


    def notify_observers(self, notification):
        """
        Notify the C{IObservers} for a particular C{INotification}.

        All previously attached C{IObservers} for this C{INotification}'s
        list are notified and are passed a reference to the C{INotification} in
        the order in which they were registered.

        @param notification: the C{INotification} to notify C{IObservers} of.
        """
        observers = self.observer_map.get(notification.get_name(), [])[:]
        for obsvr in observers:
            obsvr.notify_observer(notification)


    def remove_observer(self, notification_name, notify_context):
        """
        Remove the observer for a given notify_context from an observer list for a given Notification name.

        @param notification_name: which observer list to remove from
        @param notify_context: remove the observer with this object as its notify_context
        """
        observers = self.observer_map[notification_name]

        for i in range(len(observers)-1, -1, -1):
            if observers[i].compare_notify_context(notify_context):
                observers.pop(i)
                break

        if not observers:
            del self.observer_map[notification_name]


    def register_mediator(self, mediator):
        """
        Register an C{IMediator} instance with the C{View}.

        Registers the C{IMediator} so that it can be retrieved by name,
        and further interrogates the C{IMediator} for its
        C{INotification} interests.

        If the C{IMediator} returns any C{INotification}
        names to be notified about, an C{Observer} is created encapsulating
        the C{IMediator} instance's C{handle_notification} method
        and registering it as an C{Observer} for all C{INotifications} the
        C{IMediator} is interested in.

        @param mediator: a reference to the C{IMediator} instance
        """
        # do not allow re-registration (you must to remove_mediator fist)
        if mediator.get_mediator_name() in self.mediator_map:
            return

        mediator.initialize_notifier(self.multiton_key)
        self.mediator_map[mediator.get_mediator_name()] = mediator
        interests = mediator.list_notification_interests()
        if len(interests) > 0:
            obsvr = Observer(mediator.handle_notification, mediator)

            for i in range(0,len(interests)):
                self.register_observer(interests[i], obsvr)

        mediator.on_register()


    def retrieve_mediator(self, mediator_name):
        """
        Retrieve an C{IMediator} from the C{View}.

        @param mediator_name: the name of the C{IMediator} instance to retrieve.
        @return: the C{IMediator} instance previously registered with the given C{mediator_name}.
        """
        return self.mediator_map.get(mediator_name,None)


    def remove_mediator(self, mediator_name):
        """
        Remove an C{IMediator} from the C{View}.

        @param mediator_name: name of the C{IMediator} instance to be removed.
        @return: the C{IMediator} that was removed from the C{View}
        """
        for notificationName in self.observer_map.keys():
            observers = self.observer_map[notificationName]
            for i in range(len(observers)-1, -1, -1):
                if observers[i].compare_notify_context(self.retrieve_mediator(mediator_name)):
                    observers.pop(i)

            if not observers:
                del self.observer_map[notificationName]

        mediator = self.mediator_map.get(mediator_name,None)

        if mediator is not None:
            del self.mediator_map[mediator_name]
            mediator.on_remove()
        return mediator


    def has_mediator(self, mediator_name):
        """
        Check if a Mediator is registered or not

        @param mediator_name: the name of the C{IMediator}
        @return: whether a Mediator is registered with the given C{mediator_name}.
        """
        return self.mediator_map.get(mediator_name,None) is not None
