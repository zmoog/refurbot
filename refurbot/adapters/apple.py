from typing import List

from refurbished import Store
from refurbished.parser import Product


class RefurbishedStoreAdapter:
    def search(self, country: str, product: str) -> List[Product]:
        products: List[Product]
        store = Store(country)

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

        return list(products)


class ProductNotSupported(Exception):
    pass
