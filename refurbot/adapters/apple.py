from typing import Generator

from refurbished import Store
from refurbished.parser import Product


class RefurbishedStoreAdapter:
    def search(self, country: str, product: str) -> Generator[Product, None, None]:
        store = Store(country)

        products: Generator[Product, None, None]
        if product == 'ipad':
            products = store.get_ipads()
        elif product == 'iphone':
            products = store.get_iphones()
        elif product == 'mac':
            products = store.get_macs()
        else:
            raise ProductNotSupported(
                f"'{product}'' is not yet supported by this adapter"
            )

        return products

class ProductNotSupported(Exception):
    pass
