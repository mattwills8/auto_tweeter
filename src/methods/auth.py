import re
from twython import Twython
from src.secrets import *
import os

APP_KEY = os.getenv('APP_KEY', "")
APP_SECRET = os.getenv('APP_SECRET', "")
callback_uri = 'https://127.0.0.1/callback'  # call-back for localhost


def auth(app_key, app_secret):
    callback_uri = 'https://127.0.0.1/callback'

    check_app_key_and_secret(app_key,app_secret)

    twitter = Twython(app_key, app_secret)
    auth = twitter.get_authentication_tokens(callback_url=callback_uri)

    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

    print 'Follow link: ' + str(auth['auth_url'])

    redirect_url = raw_input('Paste the full redirect URL here.')

    oauth_verifier = re.search("(?<=oauth_verifier=).*", redirect_url).group(0)

    twitter = Twython(app_key, app_secret, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    final_step = twitter.get_authorized_tokens(oauth_verifier)

    F_OAUTH_TOKEN = final_step['oauth_token']
    F_OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

    print 'AUTHORISED'
    print 'ACCESS TOKEN: ' + F_OAUTH_TOKEN
    print 'ACCESS TOKEN SECRET: ' + F_OAUTH_TOKEN_SECRET
    return F_OAUTH_TOKEN, F_OAUTH_TOKEN_SECRET


def check_app_key_and_secret(app_key, app_secret):
    if app_key == "":
        print "Need to set App Key as env variable"
    elif app_secret == "":
        print "Need to set App Secret as env variable"

def auth_needed(access_token, access_token_secret):
    if access_token == "":
        return True
    elif access_token_secret == "":
        return True
    else:
        return False

