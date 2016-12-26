# methods for uploading media

from twython import TwythonError


def upload_video(client, path_to_video):
    """
    :param path_to_video: video pathname in finder
    attempts to upload video to twitter
    :return JSON response from video upload
    """

    video = open('r' + path_to_video, 'rb')

    print 'Uploading video...'

    try:
        response = client.upload_video(media=video, media_type='video/mp4')
        return response
    except TwythonError as e:
        print e


def process_video(client, account_id, video_media_id, title=None):
    """
    :param video_media_id: media_id_string from video upload
    :param title: a title for the video
    processes the video for use on twitter app cards
    :return: JSON response for video processing
    """

    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/videos'.format(account_id)

    method = 'POST'
    params = {
        'video_media_id': video_media_id,
        'title': title
    }
    try:
        response = client.request(endpoint=endpoint, method=method, params=params)
        return response
    except TwythonError as e:
        print e


def upload_image(client, path_to_image):
    """
    :param path_to_image: pathname from finder of image to be uploaded
    uploads image to twitter
    :return: JSON response from image upload
    """

    photo = open('r' + path_to_image, 'rb')

    print 'Uploading Image...'

    try:
        response = client.upload_media(media=photo)
        return response
    except TwythonError as e:
        print e
