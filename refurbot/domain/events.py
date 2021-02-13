from dataclasses import dataclass
from typing import List

from refurbished.parser import Product


class Event:
    pass


@dataclass
class DealsFound(Event):
    country: str
    product: str
    deals: List[Product]
    best_deal: Product


@dataclass
class DealsNotFound(Event):
    country: str
    product: str
