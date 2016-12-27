import argparse

from methods.sandbox import *
from src.methods.auth import *
from src.methods.promote_tweets import *


def main(sandbox_mode):

    if auth_needed(ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
        print "Need to log in..."
        [access_token, access_token_secret] = auth(APP_KEY, APP_SECRET)
    else:
        print "Checking log in..."
        access_token = ACCESS_TOKEN
        access_token_secret = ACCESS_TOKEN_SECRET

    client = Twython(APP_KEY, APP_SECRET, access_token, access_token_secret)

    account_id = ACCOUNT_ID

    if sandbox_mode:
        account_id = create_sandbox_account(client)

    try:
        print 'Available cards:'
        print json.dumps(get_available_video_cards(client, account_id, name_and_url_only=True), indent=4)

        print 'Available campaigns: '
        print [campaign['campaign_name'] for campaign in get_campaigns_info(client, account_id, draft=False)]

        copy_list = [x for x in map(str, raw_input('Input tweet copy: ').split(";"))]
        card_url = str(raw_input('Select card URL: '))
        campaign_names = [x for x in map(str, raw_input('Select campaign names:').split(";"))]

        tweet_ids = [create_tweet_with_card(client, account_id, card_url=card_url, copy=copy)['data']['id_str'] for copy
                     in copy_list]

        print json.dumps(promote_tweets(client, account_id, campaign_names=campaign_names, tweet_ids=tweet_ids),
                         indent=4)

    finally:
        if sandbox_mode:
            delete_sandbox_account(client, account_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sandbox', help='Sandbox mode', action='store_true') #why does store_true seem to make it false?
    args = parser.parse_args()
    main(args.sandbox)
