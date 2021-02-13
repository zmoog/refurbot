import logging

from typing import Any, Callable, Dict, List, Type

from refurbot.domain import commands, events
from refurbot.services import unit_of_work
from refurbot.services.handlers import no_op

logger = logging.getLogger(__name__)


class MessageBus:

    def __init__(
        self,
        uow: unit_of_work.UnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable]
    ):
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.uow = uow

    def handle(self, message, context: Dict[str, Any] = {}):
        self.queue = [message]

        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self._handle_event(message, context)
            if isinstance(message, commands.Command):
                self._handle_command(message, context)

    def _handle_event(
        self,
        event: events.Event,
        context: Dict[str, Any],
    ):
        for handler in self.event_handlers.get(type(event), [no_op]):
            handler(event, self.uow, context)

    def _handle_command(
        self,
        command:
        commands.Command,
        context: Dict[str, Any],
    ):
        if type(command) not in self.command_handlers:
            raise Exception(f"No handler for command {command}")

        handler = self.command_handlers.get(type(command))
        events = handler(command, self.uow, context)
        self.queue.extend(events)
