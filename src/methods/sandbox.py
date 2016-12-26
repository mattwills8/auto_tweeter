import json


def create_sandbox_account(client):
    """
    :return  New sandbox account for current client.
            pretty printed dictionary of new sandbox account info:
    """

    response = client.request('https://ads-api-sandbox.twitter.com/1/accounts/', 'post')
    print json.dumps(response, indent=4)


def delete_sandbox_account(client, sandbox_account_id):
    """
    :param sandbox_account_id:
    :return deletes sadnbox account with specified id:
    """
    endpoint = 'https://ads-api-sandbox.twitter.com/1/accounts/{}'.format(sandbox_account_id)
    response = client.request(endpoint, 'delete')
    print json.dumps(response, indent=4)
