from typing import Any, Dict, List

from refurbot.domain import commands, events
from refurbot.services.unit_of_work import UnitOfWork


#
# Command handlers
#

def search_deals(
    cmd: commands.SearchDeals,
    uow: UnitOfWork,
    context: Dict[str, Any]) -> List[events.Event]:

    with uow:
        deals = uow.refurbished_store.search(cmd.country, cmd.product)

        if not deals:
            return [events.DealsNotFound(
                country=cmd.country,
                product=cmd.product,
            )]

        # get the deal, arbitrarily defined as the one with the 
        # max saving percentage
        the_best_deal = max(deals, key=lambda deal: deal.saving_percentage)

        return [events.DealsFound(
            country=cmd.country,
            product=cmd.product,
            deals=list(deals),
            best_deal=the_best_deal,
        )]


#
# Event handlers
#
def no_op(
    event: events.Event,
    _: UnitOfWork,
    context: Dict[str, Any] = {}):

    print(f"No handler was associated to the {event} event.")


#
# Event handlers
#
def tweet_deals(
    event: events.DealsFound,
    uow: UnitOfWork,
    context: Dict[str, Any]):

    with uow:
        text = f"""Hey, here's the best deal I could found today for the {event.product} in the {event.country} store:

{event.best_deal.name[:50]} is now at {event.best_deal.price:.0f} instead of {event.best_deal.previous_price:.0f}.

You're saving {event.best_deal.savings_price:.0f} — it's {event.best_deal.saving_percentage * 100:.0f}% OFF.

Learn more visiting:
{event.best_deal.url}
"""
        uow.twitter.update_status(text)
