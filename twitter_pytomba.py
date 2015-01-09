# coding: utf-8

from requests_oauthlib import OAuth1

from pytomba import ApiClient, BaseClientAdapter


class TwitterClientAdapter(BaseClientAdapter):
    api_root = 'https://api.twitter.com/1.1'
    resource_mapping = {
        'user_timeline': {
            'resource': 'statuses/user_timeline.json',
            'methods': ['get'],
        },
        'statuses_show': {
            'resource': 'statuses/show/{id}.json',
            'methods': ['get']
        }
    }

    def get_request_kwargs(self, api_params):
        client_key = api_params.get('api_key')
        return {
            'auth': OAuth1(client_key, 
                client_secret=api_params.get('api_secret'),
                resource_owner_key=api_params.get('access_token'),
                resource_owner_secret=api_params.get('access_token_secret'))
        }


TwitterApiClient = ApiClient(TwitterClientAdapter())

from decouple import config


cli = TwitterApiClient(api_params={
        'api_key': config('API_KEY'),
        'api_secret': config('API_SECRET'),
        'access_token': config('ACCESS_TOKEN'),
        'access_token_secret':  config('ACCESS_TOKEN_SECRET'),
    })

# status = cli.statuses_show({'id': 515109944312733696})
# print(status.user.url())

timeline = cli.user_timeline.get()
# print timeline[0].text.list_nodes()
# print timeline[0].list_nodes()
