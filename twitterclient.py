# from app import twitter
from config import USER_CREDENTIALS
from flask_oauthlib.client import OAuth

class TwitterClient(OAuth.remote_app):
    """
    Not very tidy; Flask-OAuthlib requires tokengetter decorator, which means
    Twitter remote app must be declared global.
    """
    def __init__(self, name, consumer_key, consumer_secret, base_url,
                request_token_url, access_token_url, authorize_url,
                user_credentials=None):
        super(TwitterClient, self).__init__(name,
                                            consumer_key=consumer_key,
                                            consumer_secret=consumer_secret,
                                            base_url=base_url,
                                            request_token_url=request_token_url,
                                            access_token_url=access_token_url,
                                            authorize_url=authorize_url)
        self.credentials=user_credentials
        tokengetter(self.get_token)

    def follow(user_id):
        resp = self.post('friendships/create.json', data={'user_id':user_id,
            'follow':True})
        return resp

    def get_followers():
        resp = self.get('followers/ids.json',
                data={'screen_name':USER_CREDENTIALS['twitter']['screen_name']})
        return resp.data['ids']

    def get_followed():
        resp = self.get('friends/ids.json',
                data={'screen_name':USER_CREDENTIALS['twitter']['screen_name']})
        return resp.data['ids']

    def post_status(status):
        self.post('statuses/update.json', data={'status':status})

    def get_token(self):
        cred = self.credentials
        if cred is None:
            return ('','')
        return (cred['access-token'], cred['access-token-secret'])
