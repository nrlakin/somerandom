from app import twitter
from config import USER_CREDENTIALS
from flask_oauthlib.client import OAuth

class TwitterClient():
    """
    Not very tidy; Flask-OAuthlib requires tokengetter decorator, which means
    Twitter remote app must be declared global.
    """
    def __init__(self):
        pass

    def follow(user_id):
        resp = twitter.post('friendships/create.json', data={'user_id':user_id,
            'follow':True})
        return resp

    def get_followers():
        resp = twitter.get('followers/ids.json',
                data={'screen_name':USER_CREDENTIALS['twitter']['screen_name']})
        return resp.data['ids']

    def get_followed():
        resp = twitter.get('friends/ids.json',
                data={'screen_name':USER_CREDENTIALS['twitter']['screen_name']})
        return resp.data['ids']

    def post_status(status):
        twitter.post('statuses/update.json', data={'status':status})

    @twitter.tokengetter
    def get_token(self):
        cred = USER_CREDENTIALS['twitter']
        return (cred['access-token'], cred['access-token-secret'])
