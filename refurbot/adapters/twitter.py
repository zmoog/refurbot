import tweepy

from refurbot import config


class TwitterAdapter:

    def __init__(self) -> None:
        auth = tweepy.OAuthHandler(
            config.TWITTER_API_KEY,
            config.TWITTER_API_SECRET
        )
        auth.set_access_token(
            config.TWITTER_ACCESS_KEY,
            config.TWITTER_ACCESS_SECRET,
        )
        self._api = tweepy.API(auth)

    def update_status(self, text: str):
        self._api.update_status(text)
