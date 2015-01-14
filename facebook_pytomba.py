# coding: utf-8

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
        'user_likes': {
            'resource': '{user}/likes',
            'methods': ['get'],
        },
    }

    def get_request_kwargs(self, api_params):
        client_id = api_params.get('client_id')
        return {
            'auth': OAuth2(client_id, 
                token={
                    'access_token': api_params.get('access_token'),
                    'token_type': 'Bearer'})
        }

    def get_iterator_list(self, response_data):
        return response_data['data']

    def get_iterator_next_url(self, response_data):
        paging = response_data.get('paging')
        if not paging:
            return
        
        return paging.get('next')


FacebookApiClient = ApiClient(FacebookClientAdapter())

from decouple import config


api = FacebookApiClient(api_params={
        'client_id': config('FACEBOOK_CLIENT_ID'),
        'access_token': config('FACEBOOK_ACCESS_TOKEN'),
    })

user_likes = api.user_likes(url_params={'user': 'me'}).get()

# print user_likes.data

# for item in user_likes:
#     print item.name.data()


# print user.data
# print user.name.data

# user = api.user
# print user.data
# user = user.get()
# print user.data
