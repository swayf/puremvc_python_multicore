"""
 PureMVC Multicore Port, pep8 by Oleg Butovich <obutovich@gmail.com>
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""

from puremvc_multicore.interfaces import ICommand, INotifier
from puremvc_multicore.patterns.notifier import Notifier


class MacroCommand(Notifier, ICommand, INotifier):
    """
    A base C{ICommand} implementation that executes other C{ICommand}s.

    A C{MacroCommand} maintains an list of C{ICommand} Class references called I{SubCommands}.

    When C{execute} is called, the C{MacroCommand}
    instantiates and calls C{execute} on each of its I{SubCommands} turn.
    Each I{SubCommand} will be passed a reference to the original
    C{INotification} that was passed to the C{MacroCommand}'s
    C{execute} method.

    Unlike C{SimpleCommand}, your subclass
    should not override C{execute}, but instead, should
    override the C{initialize_macro_command} method,
    calling C{add_sub_command} once for each I{SubCommand}
    to be executed.

    @see: L{Controller<puremvc_multicore.core.controller.Controller>}
    @see: L{Notification<puremvc_multicore.patterns.observer.Notification>}
    @see: L{SimpleCommand<puremvc_multicore.patterns.command.SimpleCommand>}
    """

    sub_commands = None

    def __init__(self):
        """
        MacroCommand Constructor

        You should not need to define a constructor,
        instead, override the C{initialize_macro_command}
        method.
        """
        self.sub_commands = []
        self.initialize_macro_command()

    def initialize_macro_command(self):
        """
        Initialize the C{MacroCommand}.

        In your subclass, override this method to
        initialize the C{MacroCommand}'s I{SubCommand}
        list with C{ICommand} class references like
        this:

        Note that I{SubCommand}s may be any C{ICommand} implementer,
        C{MacroCommand}s or C{SimpleCommands} are both acceptable.
        """
        pass

    def add_sub_command(self, command_class_ref):
        """
        Add a I{SubCommand}.

        The I{SubCommands} will be called in First In/First Out (FIFO)
        order.

        @param command_class_ref: a reference to the C{Class} of the C{ICommand}.
        """
        self.sub_commands.append(command_class_ref)


    def execute(self, notification):
        """
        Execute this C{MacroCommand}'s I{SubCommands}.

        The I{SubCommands} will be called in First In/First Out (FIFO)
        order.

        @param notification: the C{INotification} object to be passsed to each I{SubCommand}.
        """
        while len(self.sub_commands) > 0:
            command_class_ref = self.sub_commands.pop(0)
            command_instance = command_class_ref()
            command_instance.execute(notification)


class SimpleCommand(Notifier, ICommand, INotifier):
    """
    A base C{ICommand} implementation.

    Your subclass should override the C{execute}
    method where your business logic will handle the C{INotification}.

    @see: L{Controller<puremvc_multicore.core.controller.Controller>}
    @see: L{Notification<puremvc_multicore.patterns.observer.Notification>}
    @see: L{MacroCommand<puremvc_multicore.patterns.command.MacroCommand>}
    """

    def execute(self, notification):
        """
        Fulfill the use-case initiated by the given C{INotification}.

        In the Command Pattern, an application use-case typically
        begins with some user action, which results in an C{INotification} being broadcast, which
        is handled by business logic in the C{execute} method of an
        C{ICommand}.

        @param notification: the C{INotification} to handle.
        """
        pass
