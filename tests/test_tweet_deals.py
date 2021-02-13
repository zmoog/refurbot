from decimal import Decimal

from refurbished.parser import Product

from refurbot.domain import commands
from refurbot.adapters import apple, twitter
from refurbot.services.messagebus import MessageBus


def test_tweet_deals(mocker,
                     messagebus: MessageBus,
                     refurbished_adapter: apple.RefurbishedStoreAdapter,
                     twitter_adapter: twitter.TwitterAdapter):
    #
    # patch refurbished store adapter
    #
    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [
        [Product(name='MacBook Pro 13,3" ricondizionato con Intel Core i5 quad-core a 2,4GHz e display Retina - Argento',
                 url="https://t.co/2MgYackLWP?amp=1",
                 price=Decimal(1979.00),
                 previous_price=Decimal(1679.00),
                 savings_price=300,
                 saving_percentage=0.15)]
    ]

    #
    # patch twitter adapter
    #
    mocker.patch.object(twitter_adapter, 'update_status')
    twitter_adapter.update_status.side_effect = [None]

    #
    # Run the command
    #
    messagebus.handle(commands.SearchDeals("it", "mac"), {})

    #
    # Verify the result
    #
    twitter_status = """Hey, here's the best deal I could found today for the mac in the it store:

MacBook Pro 13,3" ricondizionato con Intel Core i5 is now at 1979 instead of 1679.

You're saving 300 — it's 18% OFF.

Learn more visiting:
https://t.co/2MgYackLWP?amp=1
"""

    twitter_adapter.update_status.assert_called_once_with(
        twitter_status
    )


def test_deals_not_found(mocker,
                         messagebus: MessageBus,
                         refurbished_adapter: apple.RefurbishedStoreAdapter,
                         twitter_adapter: twitter.TwitterAdapter):

    #
    # patch refurbished store adapter
    #
    mocker.patch.object(refurbished_adapter, "search")
    refurbished_adapter.search.side_effect = [
        []  # no deals for this product today ¯\_(ツ)_/¯
    ]

    #
    # patch twitter adapter
    #
    mocker.patch.object(twitter_adapter, 'update_status')
    twitter_adapter.update_status.side_effect = [None]

    #
    # Run the command
    #
    messagebus.handle(commands.SearchDeals("it", "mac"), {})

    #
    # Verify the result
    #
    twitter_adapter.update_status.assert_not_called()
