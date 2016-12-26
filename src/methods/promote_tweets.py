# process for creating promoted tweets

from src.methods.campaigns import *
from src.methods.uploading import *


def get_available_video_cards(client, account_id, count=20, include_deleted=False, name_and_url_only=True):
    """
    :param count: how many cards to return
    :param include_deleted: include deleted cards
    :param name_and_url_only: if True then the method will return a dict of cards with name and preview_id
                                if False, returns JSON response with all card info
    """

    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/cards/video_app_download'.format(account_id)

    params = {
        'count': count,
        'with_deleted': include_deleted
    }

    try:
        response = client.request(endpoint=endpoint, params=params)
    except TwythonError as e:
        print e

    name_url = {}

    for card in response['data']:
        name_url['{}'.format(card['name'])] = card['preview_url']

    if name_and_url_only:
        return name_url
    else:
        return response


def create_tweet_with_card(client, account_id, card_url=None, copy=None):
    """
    :param card_url: preview url of previously made app card
    :param copy: copy to be displayed with the tweet
    creates promotable tweet using previously created card and specified copy
    :return: JSON response from tweet creation
    """

    status = copy + " " + card_url

    while True:

        # break if status length exceeds twitter allowance
        if len(status) > 140:
            print 'Copy and URL exceed maximum length for card with copy {}'.format(copy)
            break

        endpoint = 'https://ads-api.twitter.com/1/accounts/{}/tweet'.format(account_id)

        method = 'POST'
        params = {
            'status': status,

            # note this only works if you have the correct permissions from the account owner
            'as_user_id': 98639399
        }

        try:
            response = client.request(endpoint=endpoint, method=method, params=params)
            return response
        except TwythonError as e:
            print e
            break

        break


def promote_tweets(client, account_id, campaign_names=[], tweet_ids=[]):
    """
    :param campaigns: a list of campaign names to push tweets to
    :param tweet_ids: ids of tweets to be promoted in campaigns
        promotes all specified tweets in all specified campaigns
    :return: JSON response from tweet promotion
    """

    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/promoted_tweets'.format(account_id)

    campaigns = get_campaigns_info(client, account_id, campaigns_wanted=campaign_names, draft=False)

    for campaign in campaigns:

        method = 'POST'
        params = {
            'line_item_id': campaign['line_item_id'],
            'tweet_ids': tweet_ids
        }

        try:
            response = client.request(endpoint=endpoint, method=method, params=params)
            return response
        except TwythonError as e:
            print e
