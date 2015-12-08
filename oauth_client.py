flask import current_app
from app import app, oauth, twitter

@twitter.tokengetter
def get_token(self):
    cred = current_app.config[USER_CREDENTIALS]
    return (cred['access-token'], cred['access-token-secret'])
