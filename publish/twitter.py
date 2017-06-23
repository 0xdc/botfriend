"""Twitter delivery mechanism for botfriend."""
from nose.tools import set_trace
import tweepy
from bot import Publisher

class TwitterPublisher(Publisher):
    def __init__(
            self, bot, full_config, kwargs
    ):
        for key in ['consumer_key', 'consumer_secret', 'access_token',
                    'access_token_secret']:
            if not key in kwargs:
                raise ValueError(
                    "Missing required Twitter configuration key %s" % key
                )
        auth = tweepy.OAuthHandler(kwargs['consumer_key'], kwargs['consumer_secret'])
        auth.set_access_token(kwargs['access_token'], kwargs['access_token_secret'])
        self.api = tweepy.API(auth)
        
    def twitter_safe(self, content):
        # TODO: do unicode normalization
        # TODO: replace initial D., M. etc.
        return content[:140]
        
    def publish(self, post, publication):
        content = self.twitter_safe(post.content)
        # TODO: update_with_media would go here if there were attachments
        # on the Post.
        try:
            response = self.api.update_status(content)
            publication.report_success()
        except tweepy.error.TweepError, e:
            publication.report_failure(e)
        
Publisher = TwitterPublisher