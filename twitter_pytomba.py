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

    def get_iterator_list(self, response_data):
        if isinstance(response_data, list):
            return response_data

        if isinstance(response_data, dict) and 'statuses' in response_data:
            return response_data['statuses']

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs, response_data):
        iterator_list = self.get_iterator_list(response_data)
        last_item = iterator_list[-1]
        if 'id' in last_item:
            if not 'params' in iterator_request_kwargs:
                iterator_request_kwargs['params'] = {}
            iterator_request_kwargs['params']['max_id'] = last_item['id']

            return iterator_request_kwargs        


TwitterApiClient = ApiClient(TwitterClientAdapter())

from decouple import config


cli = TwitterApiClient(api_params={
        'api_key': config('TWITTER_API_KEY'),
        'api_secret': config('TWITTER_API_SECRET'),
        'access_token': config('TWITTER_ACCESS_TOKEN'),
        'access_token_secret':  config('TWITTER_ACCESS_TOKEN_SECRET'),
    })

timeline = cli.user_timeline().get(params={'screen_name': 'twitterapi'})

# status = cli.statuses_show({'id': 515109944312733696})
# print(status.user.url())

# timeline = cli.user_timeline.get()
# print timeline[0].text.list_nodes()
# print timeline[0].list_nodes()
