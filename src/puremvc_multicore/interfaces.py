"""
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""
from abc import ABCMeta, abstractmethod

class ICommand(object):
    """
    The interface definition for a PureMVC Command.

    See also:
        INotification
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, notification):
        """
        Execute the ICommand's logic to handle a given INotification.

        Args:
            notification: an INotification to handle.
        """
        pass



class IController(object):
    """
    The interface definition for a PureMVC Controller.

    In PureMVC, an IController implementer
    follows the 'Command and Controller' strategy, and
    assumes these responsibilities:

    - Remembering which ICommands
      are intended to handle which INotifications.

    - Registering itself as an IObserver with
      the View for each INotification
      that it has an ICommand mapping for.

    - Creating a new instance of the proper ICommand
      to handle a given INotification when notified by the View.

    - Calling the ICommand's execute
      method, passing in the INotification.

    See also:
        INotification, ICommand
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def registerCommand(self, notificationName, commandClassRef):
        """
        Register a particular ICommand class as the handler for a particular INotification.

        Args:
            notificationName: the name of the INotification
            commandClassRef: the Class of the ICommand
        """
        pass

    @abstractmethod
    def executeCommand(self, notification):
        """
        Execute the ICommand previously registered as the handler for INotifications with the given notification name.

        Args:
            notification: the INotification to execute the associated ICommand for
        """
        pass

    @abstractmethod
    def removeCommand(self, notificationName):
        """
        Remove a previously registered ICommand to INotification mapping.

        Args:
            notificationName: the name of the INotification to remove the ICommand mapping fo
        """
        pass

    @abstractmethod
    def hasCommand(self, notificationName):
        """
        Check if a Command is registered for a given Notification

        Args:
            notificationName: the name of the INotification
        Returns:
            whether a Command is currently registered for the given notificationName.
        """
        pass


class INotifier(object):
    """
    The interface definition for a PureMVC Notifier.

    MacroCommand, Command, Mediator and Proxy
    all have a need to send Notifications.

    The INotifier interface provides a common method called
    sendNotification that relieves implementation code of
    the necessity to actually construct Notifications.

    The Notifier class, which all of the above mentioned classes
    extend, also provides an initialized reference to the Facade
    Singleton, which is required for the convenience method
    for sending Notifications, but also eases implementation as these
    classes have frequent Facade interactions and usually require
    access to the facade anyway.

    @see: IFacade<puremvc_multicore.interfaces.IFacade>
    @see: INotification<puremvc_multicore.interfaces.INotification>
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def sendNotification(self, notificationName, body = None, type = None):
        """
        Send a INotification.

        Convenience method to prevent having to construct new
        notification instances in our implementation code.

        @param notificationName: the name of the notification to send
        @param body: the body of the notification (optional)
        @param type: the type of the notification (optional)
        """
        pass

    @abstractmethod
    def initializeNotifier(self, key):
        pass



class IFacade(INotifier):
    """
    The interface definition for a PureMVC Facade.

    The Facade Pattern suggests providing a single
    class to act as a central point of communication
    for a subsystem.

    In PureMVC, the Facade acts as an interface between
    the core MVC actors (Model, View, Controller) and
    the rest of your application.

    See also:
        IModel, IView, IController, ICommand, INotification
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def registerProxy(self, proxy):
        """
        Register an IProxy with the Model by name.

        @param proxy: the IProxy to be registered with the Model.
        """
        pass

    @abstractmethod
    def retrieveProxy(self, proxyName):
        """
        Retrieve a IProxy from the Model by name.

        @param proxyName: the name of the IProxy instance to be retrieved.
        @return: the IProxy previously registered by proxyName with the Model.
        """
        return None

    @abstractmethod
    def removeProxy(self, proxyName):
        """
        Remove an IProxy instance from the Model by name.

        @param proxyName: the IProxy to remove from the Model.
        @return: the IProxy that was removed from the Model
        """
        return None

    @abstractmethod
    def hasProxy(self, proxyName):
        """
        Check if a Proxy is registered

        @param proxyName:
        @return: whether a Proxy is currently registered with the given proxyName.
        """
        return False

    @abstractmethod
    def registerCommand(self, noteName, commandClassRef):
        """
        Register an ICommand with the Controller.

        @param noteName: the name of the INotification to associate the ICommand with.
        @param commandClassRef: a reference to the Class of the ICommand.
        """
        pass

    @abstractmethod
    def removeCommand(self, notificationName):
        """
         Remove a previously registered ICommand to INotification mapping from the Controller.

        @param notificationName: the name of the INotification to remove the ICommand mapping for
        """
        pass

    @abstractmethod
    def hasCommand(self, notificationName):
        """
        Check if a Command is registered for a given Notification

        @param notificationName: the name of the INotification
        @return: whether a Command is currently registered for the given notificationName.
        """
        return False

    @abstractmethod
    def registerMediator(self, mediator):
        """
        Register an IMediator instance with the View.

        @param mediator: a reference to the Mediator instance
        """
        pass

    @abstractmethod
    def retrieveMediator(self, mediatorName):
        """
        Retrieve an IMediator instance from the View.

        @param mediatorName: the name of the IMediator instance to retrieve
        @return: the IMediator previously registered with the given mediatorName.
        """
        return None

    @abstractmethod
    def removeMediator(self, mediatorName):
        """
        Remove a IMediator instance from the View.

        @param mediatorName: name of the IMediator instance to be removed.
        @return: the IMediator instance previously registered with the given mediatorName.
        """
        return None

    @abstractmethod
    def notifyObservers(self, note):
        """
        Notify the IObservers for a particular INotification.

        All previously attached IObservers for this INotification's list are notified
        and are passed a reference to the INotification in the order in which they were registered.

        NOTE: Use this method only if you are sending custom Notifications. Otherwise use the
        sendNotification method which does not require you to create the Notification instance.

        @param note: the INotification to notify IObservers of.
        """
        pass



class IMediator(object):
    """
    The interface definition for a PureMVC Mediator.

    In PureMVC, IMediator implementers assume these responsibilities:

    Implement a common method which returns a list of all INotifications the IMediator has interest in.

    Implement a notification callback method.

    Implement methods that are called when the IMediator is registered or removed from the View.


    Additionally, IMediators typically:

    Act as an intermediary between one or more view components such as text boxes or list controls, maintaining references and coordinating their behavior.

    In Flash-based apps, this is often the place where event listeners are
    added to view components, and their handlers implemented.

    Respond to and generate INotifications, interacting with of the rest of the PureMVC app.

    When an IMediator is registered with the IView, the IView will call the IMediator's listNotificationInterests method. The IMediator will
    return an List of INotification names which
    it wishes to be notified about.


    The IView will then create an Observer object
    encapsulating that IMediator's (handleNotification) method
    and register it as an Observer for each INotification name returned by
    listNotificationInterests.

    @see: INotification<puremvc_multicore.interfaces.INotification>
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def getMediatorName(self):
        """
        Get the IMediator instance name

        @return: the IMediator instance name
        """
        return ""

    @abstractmethod
    def getViewComponent(self):
        """
        Get the IMediator's view component.

        @return: the view component
        """
        return None

    @abstractmethod
    def setViewComponent(self, viewComponent):
        """
        Set the IMediator's view component.

        @param viewComponent: the view component
        """
        pass

    @abstractmethod
    def listNotificationInterests(self):
        """
        List INotification interests.

        @return: an List of the INotification names this IMediator has an interest in.
        """
        return []

    @abstractmethod
    def handleNotification(self, notification):
        """
        Handle an INotification.

        @param notification: the INotification to be handled
        """
        pass

    @abstractmethod
    def onRegister(self):
        """
        Called by the View when the Mediator is registered
        """
        pass

    @abstractmethod
    def onRemove(self):
        """
        Called by the View when the Mediator is removed
        """
        pass



class IModel(object):
    """
    The interface definition for a PureMVC Model.

    In PureMVC, IModel implementers provide
    access to IProxy objects by named lookup.

    An IModel assumes these responsibilities:

    Maintain a cache of IProxy instances and Provide methods for registering, retrieving, and removing IProxy instances
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def registerProxy(self, proxy):
        """
        Register an IProxy instance with the Model.

        @param proxy: an object reference to be held by the Model.
        """
        pass

    @abstractmethod
    def retrieveProxy(self, proxyName):
        """
        Retrieve an IProxy instance from the Model.

        @param proxyName: name of the IProxy instance to retrieve.
        @return: the IProxy instance previously registered with the given proxyName.
        """
        return None

    @abstractmethod
    def removeProxy(self, proxyName):
        """
        Remove an IProxy instance from the Model.

        @param proxyName: name of the IProxy instance to be removed.
        @return: the IProxy that was removed from the Model
        """
        return None

    @abstractmethod
    def hasProxy(self, proxyName):
        """
        Check if a Proxy is registered

        @param proxyName: name of the IProxy instance
        @return: whether a Proxy is currently registered with the given proxyName.
        """
        return False


class INotification(object):
    """
    The interface definition for a PureMVC Notification.

    PureMVC does not rely upon underlying event models such
    as the one provided with Flash, and ActionScript 3 does
    not have an inherent event model.

    The Observer Pattern as implemented within PureMVC exists
    to support event-driven communication between the
    application and the actors of the MVC triad.

    Notifications are not meant to be a replacement for Events
    in Flex/Flash/AIR. Generally, IMediator implementers
    place event listeners on their view components, which they
    then handle in the usual way. This may lead to the broadcast of Notifications to
    trigger ICommands or to communicate with other IMediators. IProxy and ICommand
    instances communicate with each other and IMediators by broadcasting INotifications.

    A key difference between Flash Events and PureMVC
    Notifications is that Events follow the
    'Chain of Responsibility' pattern, 'bubbling' up the display hierarchy
    until some parent component handles the Event, while
    PureMVC Notifications follow a 'Publish/Subscribe'
    pattern. PureMVC classes need not be related to each other in a
    parent/child relationship in order to communicate with one another
    using Notifications.

    @see: IView<puremvc_multicore.interfaces.IView>
    @see: IObserver<puremvc_multicore.interfaces.IObserver>
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def getName(self):
        """
        Get the name of the INotification instance.
        """
        return ""

    @abstractmethod
    def setBody(self, body):
        """
        Set the body of the INotification instance
        """
        pass

    @abstractmethod
    def getBody(self):
        """
        Get the body of the INotification instance
        """
        return None

    @abstractmethod
    def setType(self, type):
        """
        Set the type of the INotification instance
        """
        pass

    @abstractmethod
    def getType(self):
        """
        Get the type of the INotification instance
        """
        return ""

    @abstractmethod
    def str(self):
        """
        Get the string representation of the INotification instance
        """
        return ""



class IObserver(object):
    """
    The interface definition for a PureMVC Observer.

    In PureMVC, IObserver implementers assume these responsibilities:

    Encapsulate the notification (callback) method of the interested object.

    Encapsulate the notification context of the interested object.

    Provide methods for setting the interested object' notification method and context.

    Provide a method for notifying the interested object.

    PureMVC does not rely upon underlying event
    models such as the one provided with Flash,
    and ActionScript 3 does not have an inherent
    event model.

    The Observer Pattern as implemented within
    PureMVC exists to support event driven communication
    between the application and the actors of the
    MVC triad.

    An Observer is an object that encapsulates information
    about an interested object with a notification method that
    should be called when an INotification is broadcast. The Observer then
    acts as a proxy for notifying the interested object.

    Observers can receive Notifications by having their
    notifyObserver method invoked, passing
    in an object implementing the INotification interface, such
    as a subclass of Notification.

    @see: IView<puremvc_multicore.interfaces.IView>
    @see: INotification<puremvc_multicore.interfaces.INotification>
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def setNotifyMethod(self, notifyMethod):
        """
        Set the notification method.

        The notification method should take one parameter of type INotification

        @param notifyMethod: the notification (callback) method of the interested object
        """
        pass

    @abstractmethod
    def setNotifyContext(self, notifyContext):
        """
        Set the notification context.

        @param notifyContext: the notification context of the interested object
        """
        pass

    @abstractmethod
    def notifyObserver(self, notification):
        """
        Notify the interested object.

        @param notification: the INotification to pass to the interested object's notification method
        """
        pass

    @abstractmethod
    def compareNotifyContext(self, object):
        """
        Compare the given object to the notification context object.

        @param object: the object to compare.
        @return: boolean indicating if the notification context and the object are the same.
        """
        pass

class IProxy(object):
    """
    The interface definition for a PureMVC Proxy.

    In PureMVC, IProxy implementers assume these responsibilities:

    Implement a common method which returns the name of the Proxy.

    Provide methods for setting and getting the data object.

    Additionally, IProxy typically:

    Maintain references to one or more pieces of model data.
    Provide methods for manipulating that data.
    Generate INotifications when their model data changes.
    Expose their name as a public static const called NAME, if they are not instantiated multiple times.
    Encapsulate interaction with local or remote services used to fetch and persist model data.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def getProxyName(self):
        """
        Get the Proxy name

        @return: the Proxy instance name
        """
        pass

    @abstractmethod
    def setData(self, data):
        """
        Set the data object

         @param data: the data object
        """
        pass

    @abstractmethod
    def getData(self):
        """
        Get the data object

         @return: the data as type Object
        """
        pass

    @abstractmethod
    def onRegister(self):
        """
        Called by the Model when the Proxy is registered
        """
        pass

    @abstractmethod
    def onRemove(self):
        """
        Called by the Model when the Proxy is removed
        """
        pass



class IView(object):
    """
    The interface definition for a PureMVC View.

    In PureMVC, IView implementers assume these responsibilities:

    In PureMVC, the View class assumes these responsibilities:

    Maintain a cache of IMediator instances.

    Provide methods for registering, retrieving, and removing IMediators.

    Managing the observer lists for each INotification in the application.

    Providing a method for attaching IObservers to an INotification's observer list.

    Providing a method for broadcasting an INotification.

    Notifying the IObservers of a given INotification when it broadcast.

    @see: IMediator<puremvc_multicore.interfaces.IMediator>
    @see: IObserver<puremvc_multicore.interfaces.IObserver>
    @see: INotification<puremvc_multicore.interfaces.INotification>
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def registerObserver(self, notificationName, observer):
        """
        Register an IObserver to be notified of INotifications with a given name.

        @param notificationName: the name of the INotifications to notify this IObserver of
        @param observer: the IObserver to register
        """
        pass

    @abstractmethod
    def notifyObservers(self, notification):
        """
        Notify the IObservers for a particular INotification.

        All previously attached IObservers for this INotification's
        list are notified and are passed a reference to the INotification in
        the order in which they were registered.</P>

        @param notification: the INotification to notify IObservers of.
        """
        pass

    @abstractmethod
    def registerMediator(self, mediator):
        """
        Register an IMediator instance with the View.

        Registers the IMediator so that it can be retrieved by name,
        and further interrogates the IMediator for its
        INotification interests.

        If the IMediator returns any INotification
        names to be notified about, an Observer is created encapsulating
        the IMediator instance's handleNotification method
        and registering it as an Observer for all INotifications the
        IMediator is interested in.

        @param mediator: a reference to the IMediator instance
        """
        pass

    @abstractmethod
    def retrieveMediator(self, mediatorName):
        """
        Retrieve an IMediator from the View.

        @param mediatorName: the name of the IMediator instance to retrieve.
        @return: the IMediator instance previously registered with the given mediatorName.
        """
        pass

    @abstractmethod
    def removeMediator(self, mediatorName):
        """
        Remove an IMediator from the View.

        @param mediatorName: name of the IMediator instance to be removed.
        @return: the IMediator that was removed from the View
        """
        pass

    @abstractmethod
    def hasMediator(self, mediatorName):
        """
        Check if a Mediator is registered or not

        @param mediatorName: name of the IMediator
        @return: whether a Mediator is registered with the given mediatorName.
        """
        pass
