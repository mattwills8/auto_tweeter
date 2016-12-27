# methods for creating app cards

import datetime
import re

from src.methods.uploading import *


# VIDEOS

def video_app_card(client, account_id, name, video_uuid, app_country_code, app_cta, iphone_app_idsometimes=None,
                   ipad_app_idsometimes=None, googleplay_app_idsometimes=None):
    """
    :param app_cta: app call to action
    :param app_country_code: country code of app
    :param video_uuid: id of processed video
    :param name: name of card - this should be taken from the end of the video pathname and timestamped
    creates a video app card from uploaded and processed video
    note: consider here generalising parameters to other apps
    :return: JSON response from card creation
    """

    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/cards/video_app_download'.format(account_id)

    method = 'POST'
    params = {
        'name': name,
        'app_country_code': app_country_code,
        'iphone_app_idsometimes': iphone_app_idsometimes,
        'ipad_app_idsometimes': ipad_app_idsometimes,
        'googleplay_app_idsometimes': googleplay_app_idsometimes,
        'app_cta': app_cta,
        'video_id': video_uuid

    }

    try:
        response = client.request(endpoint=endpoint, method=method, params=params)
        return response
    except TwythonError as e:
        print e


def video_to_app_card(client, account_id, path_to_video):
    """
    :param path_to_video: pathfile for video to be made into app card
        creates a video app card using params specified in video_app_card method
        handles whole process form uploading video to card creation
    :return: JSON response from card creation
    """

    video = upload_video(client, 'r' + path_to_video)

    title = re.search('[^/]*$', 'r' + path_to_video).group(0)
    title = title + ' ' + str(datetime.date.today())

    processed_video = process_video(client, account_id, video['media_id_string'], title=title)

    card = video_app_card(client, account_id, processed_video['data']['id'], name=title)

    return card


# IMAGES


def image_app_card(client, account_id, card_name, image_id, app_country_code, app_cta, iphone_app_idsometimes=None,
                   ipad_app_idsometimes=None, googleplay_app_idsometimes=None):
    """
    :param image_id: id of uploaded image
    :param name: name of card - this should be the end of the image pathname followed by a timestamp
        creates image app card
        note: consider generalising params to all apps
    :return: JSON response from card creation
    """

    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/cards/image_app_download'.format(account_id)

    method = 'POST'
    params = {
        'name': card_name,
        'app_country_code': app_country_code,
        'iphone_app_idsometimes': iphone_app_idsometimes,
        'ipad_app_idsometimes': ipad_app_idsometimes,
        'googleplay_app_idsometimes': googleplay_app_idsometimes,
        'app_cta': app_cta,
        'wide_app_image_media_id': image_id
    }

    try:
        response = client.request(endpoint=endpoint, method=method, params=params)
        return response
    except TwythonError as e:
        print e


def image_to_app_card(client, account_id, path_to_image):
    """
    :param path_to_image: pathname of image to be made into app card
        creates an image app card using params specified in image_app_card method
        handles whole process form uploading image to card creation
    :return JSON response from card creation
    """

    image = upload_image(client, 'r' + path_to_image)

    title = re.search('[^/]*$', 'r' + path_to_image).group(0)
    title = title + ' ' + str(datetime.date.today())

    card = image_app_card(client, account_id, image['media_id_string'], name=title)

    return card
