from flask_oauthlib.client import OAuthRemoteApp

class TwitterClient(OAuthRemoteApp):
    def __init__(self, oauth, name, consumer_key, consumer_secret, base_url,
                request_token_url, access_token_url, authorize_url,
                user_credentials, logger):
        super(TwitterClient, self).__init__(oauth,
                                            name,
                                            consumer_key=consumer_key,
                                            consumer_secret=consumer_secret,
                                            base_url=base_url,
                                            request_token_url=request_token_url,
                                            access_token_url=access_token_url,
                                            authorize_url=authorize_url)
        self.credentials=user_credentials
        self.screen_name = user_credentials['screen_name']
        self.logger = logger
        super(TwitterClient, self).tokengetter(self.get_token)

    def follow(self, user_id):
        resp = self.post('friendships/create.json', data={'user_id':user_id,
            'follow':True})
        if resp.data.get('errors') is not None:
            errors = resp.data.get('errors')
            for error in errors:
                self.logger.info("Error following: " + str(error['message']))
        return resp

    def get_followers(self):
        resp = self.get('followers/ids.json',
                data={'screen_name':self.screen_name})
        if resp.data.get('errors') is not None:
            errors = resp.data.get('errors')
            for error in errors:
                self.logger.info("Error getting followers: " + str(error['message']))
        return resp.data.get('ids')

    def get_followed(self):
        resp = self.get('friends/ids.json',
                data={'screen_name':self.screen_name})
        if resp.data.get('errors') is not None:
            errors = resp.data.get('errors')
            for error in errors:
                self.logger.info("Error getting followed: " + str(error['message']))
        return resp.data.get('ids')

    def post_status(self, status):
        resp = self.post('statuses/update.json', data={'status':status})
        if resp.data.get('errors') is not None:
            errors = resp.data.get('errors')
            for error in errors:
                self.logger.info("Error posting status: " + str(error['message']))
        return resp

    def get_token(self):
        cred = self.credentials
        if cred is None:
            return ('','')
        return (cred['access-token'], cred['access-token-secret'])
