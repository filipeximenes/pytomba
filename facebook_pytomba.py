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

    def get_request_kwargs(self, api_params):
        client_id = api_params.get('client_id')
        return {
            'auth': OAuth2(client_id, 
                token={
                    'access_token': api_params.get('access_token'),
                    'token_type': 'Bearer'})
        }


FacebookApiClient = ApiClient(FacebookClientAdapter())


api = FacebookApiClient(api_params={
        'client_id': '1495124414107995',
        'access_token': 'CAAVPzseZAEVsBAFS83pCuTBZA5ZAeShxMZBmvSqgSMeWo2MxBZCZAZC9dkpsLXwQlvd2kcTUtFKyy4eIkMs21UXqIeTXgPqeRZCftTTm4CDRUQe4755G5dZBrNzNmAER4w2FQfsrifIupYMIe4VkO4pQhECVZBAOsajEqjiiijDI4KuJ3kZCa3zvgAMVhHoZCduWjZC4l2wUST5a3P4ehn5nksuJZC',
    })

user = api.user(url_params={'user': 'me'}).get()
# print user.data
# print user.name.data

# user = api.user
# print user.data
# user = user.get()
# print user.data
