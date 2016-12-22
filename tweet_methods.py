from twython import Twython, TwythonError
import json
import re
import datetime
import os

# initiate client

APP_KEY = os.getenv('APP_KEY', '')
APP_SECRET = os.getenv('APP_SECRET', '')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', '')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET', '')

ACCOUNT_ID = os.getenv('ACCOUNT_ID', '')

twitter = Twython(APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# handling sandbox accounts

def create_sandbox_account():
    """
    :return  New sandbox account for current client.
            pretty printed dictionary of new sandbox account info:
    """

    response = twitter.request('https://ads-api-sandbox.twitter.com/1/accounts/', 'post')
    print json.dumps(response, indent=4)


SANDBOX_ACCOUNT_ID = None

sandbox = False

if sandbox:
    ACCOUNT_ID = SANDBOX_ACCOUNT_ID


def delete_sandbox_account(sandbox_account_id):
    """
    :param sandbox_account_id:
    :return deletes sadnbox account with specified id:
    """
    endpoint = 'https://ads-api-sandbox.twitter.com/1/accounts/{}'.format(sandbox_account_id)
    response = twitter.request(endpoint, 'delete')
    print json.dumps(response, indent=4)



# getting campaign and line item ids

def get_campaigns_info(campaigns_wanted=[], draft=False):
    """
    :param campaigns_wanted: list of campaigns we want info for
    :return  a list of campaigns with name, campaign id and line item id arranged in a dictionary for each
        note: no sandbox support yet
    """

    # get campaigns
    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/campaigns'.format(ACCOUNT_ID)

    response = twitter.request(endpoint=endpoint)

    if campaigns_wanted:
        campaign_names = [{'campaign_name': campaigns['name'], 'id': campaigns['id'], 'draft': "No"} for campaigns in response['data']
                          if campaigns['name'] in campaigns_wanted]
    else:
        campaign_names = [{'campaign_name': campaigns['name'], 'id': campaigns['id'], 'draft': "No"} for campaigns in response['data']]

    # get line items making sure ids match
    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/line_items'.format(ACCOUNT_ID)
    version = '1.1'

    for campaign in campaign_names:

        params = {
            'campaign_ids': campaign['id']
        }

        while True:

            try:
                response = twitter.request(endpoint=endpoint, params=params, version=version)
            except TwythonError as e:
                print e
                break

            if response['data'][0]['campaign_id'] == campaign['id']:
                campaign['line_item_id'] = response['data'][0]['id']
            else:
                print "IDs did not match"
                break

            break

    if draft:

        endpoint = 'https://ads-api.twitter.com/1/accounts/{}/campaigns'.format(ACCOUNT_ID)

        params = {
            'draft_only': True
        }

        response = twitter.request(endpoint=endpoint, params=params)

        if campaigns_wanted:
            draft_campaign_names = [{'campaign_name': campaigns['name'], 'id': campaigns['id'], 'draft': "Yes"} for campaigns
                              in response['data'] if campaigns['name'] in campaigns_wanted]
        else:
            draft_campaign_names = [{'campaign_name': campaigns['name'], 'id': campaigns['id'], 'draft': "Yes"} for campaigns
                              in response['data']]

        for campaign in draft_campaign_names:
            campaign_names.append(campaign)

    return campaign_names



# process for uploading video and creating app card

def upload_video(path_to_video):
    """
    :param path_to_video: video pathname in finder
    attempts to upload video to twitter
    :return JSON response from video upload
    """

    video = open('r' + path_to_video, 'rb')

    print 'Uploading video...'

    try:
        response = twitter.upload_video(media=video, media_type='video/mp4')
        return response
    except TwythonError as e:
        print e


def process_video(video_media_id, title=None):
    """
    :param video_media_id: media_id_string from video upload
    :param title: a title for the video
    processes the video for use on twitter app cards
    :return: JSON response for video processing
    """

    if sandbox:
        endpoint = 'https://ads-api-sandbox.twitter.com/1/accounts/{}/videos'.format(ACCOUNT_ID)
    else:
        endpoint = 'https://ads-api.twitter.com/1/accounts/{}/videos'.format(ACCOUNT_ID)

    method = 'POST'
    params = {
        'video_media_id': video_media_id,
        'title': title
    }
    try:
        response = twitter.request(endpoint=endpoint, method=method, params=params)
        return response
    except TwythonError as e:
        print e


def video_app_card(video_uuid, name=None):
    """
    :param video_uuid: id of processed video
    :param name: name of card - this should be taken from the end of the video pathname and timestamped
    creates a video app card from uploaded and processed video
    note: consider here generalising parameters to other apps
    :return: JSON response from card creation
    """

    if sandbox:
        endpoint = 'https://ads-api-sandbox.twitter.com/1/accounts/{}/cards/video_app_download'.format(ACCOUNT_ID)
    else:
        endpoint = 'https://ads-api.twitter.com/1/accounts/{}/cards/video_app_download'.format(ACCOUNT_ID)

    method = 'POST'
    params = {
        'name': name,
        'app_country_code': None,
        'iphone_app_idsometimes': None,
        'ipad_app_idsometimes': None,
        'googleplay_app_idsometimes': None,
        'app_cta': None,
        'video_id': video_uuid

    }

    try:
        response = twitter.request(endpoint=endpoint, method=method, params=params)
        return response
    except TwythonError as e:
        print e


def video_to_app_card(path_to_video):
    """
    :param path_to_video: pathfile for video to be made into app card
        creates a video app card using params specified in video_app_card method
        handles whole process form uploading video to card creation
    :return: JSON response from card creation
    """

    video = upload_video('r' + path_to_video)

    title = re.search('[^/]*$', 'r' + path_to_video).group(0)
    title = title + ' ' + str(datetime.date.today())

    processed_video = process_video(video['media_id_string'], title=title)

    card = video_app_card(processed_video['data']['id'], name=title)

    return card



# process for uploading image and creating app card

def upload_image(path_to_image):
    """
    :param path_to_image: pathname from finder of image to be uploaded
    uploads image to twitter
    :return: JSON response from image upload
    """

    photo = open('r' + path_to_image, 'rb')

    print 'Uploading Image...'

    try:
        response = twitter.upload_media(media=photo)
        return response
    except TwythonError as e:
        print e


def image_app_card(image_id, name=None):
    """
    :param image_id: id of uploaded image
    :param name: name of card - this should be the end of the image pathname followed by a timestamp
        creates image app card
        note: consider generalising params to all apps
    :return: JSON response from card creation
    """

    if sandbox:
        endpoint = 'https://ads-api-sandbox.twitter.com/1/accounts/{}/cards/image_app_download'.format(ACCOUNT_ID)
    else:
        endpoint = 'https://ads-api.twitter.com/1/accounts/{}/cards/image_app_download'.format(ACCOUNT_ID)

    method = 'POST'
    params = {
        'name': name,
        'app_country_code': None,
        'iphone_app_idsometimes': None,
        'ipad_app_idsometimes': None,
        'googleplay_app_idsometimes': None,
        'app_cta': None,
        'wide_app_image_media_id': image_id
    }

    try:
        response = twitter.request(endpoint=endpoint, method=method, params=params)
        return response
    except TwythonError as e:
        print e


def image_to_app_card(path_to_image):
    """
    :param path_to_image: pathname of image to be made into app card
        creates an image app card using params specified in image_app_card method
        handles whole process form uploading image to card creation
    :return JSON response from card creation
    """

    image = upload_image('r' + path_to_image)

    title = re.search('[^/]*$', 'r' + path_to_image).group(0)
    title = title + ' ' + str(datetime.date.today())

    card = image_app_card(image['media_id_string'], name=title)

    return card


# process for creating promoted tweets
def get_available_video_cards(count=20, include_deleted=False, name_and_url_only=True):

    """
    :param count: how many cards to return
    :param include_deleted: include deleted cards
    :param name_and_url_only: if True then the method will return a dict of cards with name and preview_id
                                if False, returns JSON response with all card info
    """

    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/cards/video_app_download'.format(ACCOUNT_ID)

    params = {
        'count': count,
        'with_deleted': include_deleted
    }

    try:
        response = twitter.request(endpoint=endpoint, params=params)
    except TwythonError as e:
        print e

    name_url = {}

    for card in response['data']:
        name_url['{}'.format(card['name'])] = card['preview_url']

    if name_and_url_only:
        return name_url
    else:
        return response


def create_tweet_with_card(card_url=None, copy=None):

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

        if sandbox:
            endpoint = 'https://ads-api-sandbox.twitter.com/1/accounts/{}/tweet'.format(ACCOUNT_ID)
        else:
            endpoint = 'https://ads-api.twitter.com/1/accounts/{}/tweet'.format(ACCOUNT_ID)

        method = 'POST'
        params = {
            'status': status,

            # note this only works if you have the correct permissions from the account owner
            'as_user_id': 98639399
        }

        try:
            response = twitter.request(endpoint=endpoint, method=method, params=params)
            return response
        except TwythonError as e:
            print e
            break

        break


def promote_tweets(campaign_names=[], tweet_ids=[]):

    """
    :param campaigns: a list of campaign names to push tweets to
    :param tweet_ids: ids of tweets to be promoted in campaigns
        promotes all specified tweets in all specified campaigns
    :return: JSON response from tweet promotion
    """

    if sandbox:
        endpoint = 'https://ads-api-sandbox.twitter.com/1/accounts/{}/promoted_tweets'.format(ACCOUNT_ID)
    else:
        endpoint = 'https://ads-api.twitter.com/1/accounts/{}/promoted_tweets'.format(ACCOUNT_ID)

    campaigns = get_campaigns_info(campaigns_wanted=campaign_names, draft=False)

    for campaign in campaigns:

        method = 'POST'
        params = {
            'line_item_id': campaign['line_item_id'],
            'tweet_ids': tweet_ids
        }

        try:
            response = twitter.request(endpoint=endpoint, method=method, params=params)
            return response
        except TwythonError as e:
            print e




def main():
    print 'Available cards:'
    print json.dumps(get_available_video_cards(name_and_url_only=True), indent=4)

    print 'Available campaigns: '
    print [campaign['campaign_name']  for campaign in get_campaigns_info(draft=False)]

    copy_list = [x for x in map(str, raw_input('Input tweet copy: ').split(";"))]
    card_url = str(raw_input('Select card URL: '))
    campaign_names = [x for x in map(str, raw_input('Select campaign names:').split(";"))]

    tweet_ids = [create_tweet_with_card(card_url=card_url, copy=copy)['data']['id_str'] for copy in copy_list]

    print json.dumps(promote_tweets(campaign_names=campaign_names, tweet_ids=tweet_ids), indent=4)

