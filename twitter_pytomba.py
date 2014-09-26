# coding: utf-8

from requests_oauthlib import OAuth1

from pytomba import ApiClient, BaseClientAdapter


class TwitterClientAdapter(BaseClientAdapter):
    api_root = 'https://api.twitter.com/1.1'
    resource_mapping = {
        'mentions_timeline': {
            'resource': 'statuses/mentions_timeline.json',
            'methods': ['get'],
        },
        'statuses_show': {
            'resource': 'statuses/show/{id}.json',
            'methods': ['get']
        }
    }

    def get_request_kwargs(self):
        client_key = self.extra_args.get('api_key')
        return {
            'auth': OAuth1(client_key, 
                client_secret=self.extra_args.get('api_secret'),
                resource_owner_key=self.extra_args.get('access_token'),
                resource_owner_secret=self.extra_args.get('access_token_secret'))
        }

    def response_to_native(self, response):
        try:
            return response.json()
        except:
            return response


TwitterApiClient = ApiClient(TwitterClientAdapter())

from decouple import config


cli = TwitterApiClient({
        'api_key': config('API_KEY'),
        'api_secret': config('API_SECRET'),
        'access_token': config('ACCESS_TOKEN'),
        'access_token_secret':  config('ACCESS_TOKEN_SECRET'),
    })

# Fetching my linkedin profile HTML
print cli.statuses_show({'id': 515109944312733696}).user.url.follow_link().data.text.encode('utf-8')

# Fetching mentions timeline
print cli.mentions_timeline()

