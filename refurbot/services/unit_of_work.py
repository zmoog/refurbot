from refurbot.adapters import apple, twitter

class UnitOfWork:

    def __init__(
        self,
        refurbished_store: apple.RefurbishedStoreAdapter,
        twitter: twitter.TwitterAdapter,
    ):
        self.refurbished_store = refurbished_store
        self.twitter = twitter

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass  # super().__exit__(*args)
