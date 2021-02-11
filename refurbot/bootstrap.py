from refurbot.adapters import apple, twitter
from refurbot.domain import commands, events
from refurbot.services.unit_of_work import UnitOfWork
from refurbot.services.messagebus import MessageBus
from refurbot.services import handlers


# Adapters
refurbished_adapter = apple.RefurbishedStoreAdapter()
twitter_adapter = twitter.TwitterAdapter()


# Unit of work
uow = UnitOfWork(
    refurbished_adapter,
    twitter_adapter,
)


# Command handlers
command_handlers = {
    commands.SearchDeals: handlers.search_deals,
}


# Event handlers
event_handlers = {
    events.DealsFound: [handlers.tweet_deals],
}


## Bootstrappers

def for_cli():
    return MessageBus(uow, event_handlers, command_handlers)

def for_lambda():
    return MessageBus(uow, event_handlers, command_handlers)
