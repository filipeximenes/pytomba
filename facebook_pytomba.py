# coding: utf-8

# import logging
# logging.basicConfig(filename='logs.log',level=logging.DEBUG)
# logging.info("aqui")

from requests_oauthlib import OAuth2

from pytomba import ApiClient, BaseClientAdapter


class FacebookClientAdapter(BaseClientAdapter):
    api_root = 'https://graph.facebook.com'
    resource_mapping = {
        'edge': {
            'resource': '{id}',
            'methods': ['get'],
        },
        'user': {
            'resource': '{user}',
            'methods': ['get'],
        },
        'user_feed': {
            'resource': '{user}/feed',
            'methods': ['get'],
        },
    }

    def get_request_kwargs(self):
        client_id = self.extra_args.get('client_id')
        return {
            'auth': OAuth2(client_id, 
                token={
                    'access_token': self.extra_args.get('access_token'),
                    'token_type': 'Bearer'})
        }


FacebookApiClient = ApiClient(FacebookClientAdapter())


api = FacebookApiClient({
        'client_id': '1495124414107995',
        'access_token': 'CAAVPzseZAEVsBAIvZAAIZB7OthClPArigGC6gHXVhjNxwzr6gDZA9GRZBeRDKC9GaqUTFiM4soZCoyWrUsvsXvx3KiVI0ZB7rqWWRx5CK4fKl4sdlXOnlR2aXOMwS1aDXVf1bo7Yerw9BgQFXKbHOSPgSGTmZCpRIt5u3eQNstGHIS2OZCvF6Ji2R7GzIabDEBYMf0UtJVxvf1j0JWuZAZCHIFn',
    })

user = api.user({'user': 'me'}).get()
# print user.data
# print user.name.data

# user = api.user
# print user.data
# user = user.get()
# print user.data
