"""
 PureMVC Multicore Port, pep8 by Oleg Butovich <obutovich@gmail.com>
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""
from puremvc_multicore.interfaces import IProxy, INotifier
from puremvc_multicore.patterns.notifier import Notifier


class Proxy(Notifier, IProxy, INotifier):
    """
    A base C{IProxy} implementation.

    In PureMVC, C{Proxy} classes are used to manage parts of the
    application's data model.

    A C{Proxy} might simply manage a reference to a local data object,
    in which case interacting with it might involve setting and
    getting of its data in synchronous fashion.

    C{Proxy} classes are also used to encapsulate the application's
    interaction with remote services to save or retrieve data, in which case,
    we adopt an asynchronous idiom; setting data (or calling a method) on the
    C{Proxy} and listening for a C{Notification} to be sent
    when the C{Proxy} has retrieved the data from the service.

    @see: L{Model<org.puremvc_multicore.as3.core.model.Model>}
    """

    NAME = None
    facade = None
    proxy_name = None
    data = None

    def __init__(self, proxy_name=None, data=None):
        """
        Proxy Constructor

        @param proxy_name: the name of the proxy instance (optional)
        @param data: the proxy data (optional)
        """
        self.__class__.NAME = self.__class__.NAME or self.__class__.__name__
        proxy_name = proxy_name or self.NAME
        if proxy_name is None:
            raise ValueError("Proxy name cannot be None")
        self.proxy_name = proxy_name
        if data:
            self.set_data(data)


    def get_proxy_name(self):
        """
        Get the Proxy name

        @return: the proxy name
        """
        return self.proxy_name


    def set_data(self, data):
        """
        Set the Proxy data

        @param data: the Proxy data object
        """
        self.data = data


    def get_data(self):
        """
        Get the proxy data

        @return: the Proxy data object
        """
        return self.data


    def on_register(self):
        """
        Called by the Model when the Proxy is registered
        """
        pass


    def on_remove(self):
        """
        Called by the Model when the Proxy is removed
        """
        pass
