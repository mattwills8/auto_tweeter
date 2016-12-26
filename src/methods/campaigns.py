#methods for handling campaigns

from twython import TwythonError

def get_campaigns_info(client, account_id, campaigns_wanted=[], draft=False):
    """
    :param campaigns_wanted: list of campaigns we want info for
    :return  a list of campaigns with name, campaign id and line item id arranged in a dictionary for each
        note: no sandbox support yet
    """

    # get campaigns
    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/campaigns'.format(account_id)

    response = client.request(endpoint=endpoint)

    if campaigns_wanted:
        campaign_names = [{'campaign_name': campaigns['name'], 'id': campaigns['id'], 'draft': "No"} for campaigns in response['data']
                          if campaigns['name'] in campaigns_wanted]
    else:
        campaign_names = [{'campaign_name': campaigns['name'], 'id': campaigns['id'], 'draft': "No"} for campaigns in response['data']]

    # get line items making sure ids match
    endpoint = 'https://ads-api.twitter.com/1/accounts/{}/line_items'.format(account_id)
    version = '1.1'

    for campaign in campaign_names:

        params = {
            'campaign_ids': campaign['id']
        }

        while True:

            try:
                response = client.request(endpoint=endpoint, params=params, version=version)
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

        endpoint = 'https://ads-api.twitter.com/1/accounts/{}/campaigns'.format(account_id)

        params = {
            'draft_only': True
        }

        response = client.request(endpoint=endpoint, params=params)

        if campaigns_wanted:
            draft_campaign_names = [{'campaign_name': campaigns['name'], 'id': campaigns['id'], 'draft': "Yes"} for campaigns
                              in response['data'] if campaigns['name'] in campaigns_wanted]
        else:
            draft_campaign_names = [{'campaign_name': campaigns['name'], 'id': campaigns['id'], 'draft': "Yes"} for campaigns
                              in response['data']]

        for campaign in draft_campaign_names:
            campaign_names.append(campaign)

    return campaign_names


