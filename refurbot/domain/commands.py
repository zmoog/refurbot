from dataclasses import dataclass


@dataclass
class Command:
    pass


@dataclass
class SearchDeals(Command):
    country: str
    product: str
