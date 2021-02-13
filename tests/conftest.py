import pytest

from refurbot import bootstrap
from refurbot.adapters import apple, twitter
from refurbot.services.messagebus import MessageBus
from refurbot.services.unit_of_work import UnitOfWork


@pytest.fixture(scope="function")
def refurbished_adapter():
    return apple.RefurbishedStoreAdapter()

@pytest.fixture(scope="function")
def twitter_adapter():
    return twitter.TwitterAdapter()

@pytest.fixture(scope="function")
def uow(refurbished_adapter, 
        twitter_adapter):
    return UnitOfWork(
        refurbished_adapter,
        twitter_adapter
    )

@pytest.fixture(scope="function")
def messagebus(uow):
    return MessageBus(
        uow,
        bootstrap.event_handlers,
        bootstrap.command_handlers,
    )