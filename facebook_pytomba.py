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
        'access_token': 'CAAVPzseZAEVsBAPIL67nvZBilBuDCLvCSjFZA4Khp2LU9w2o8lIAzZBGuOO07vVpNziykOwUZCpeNdYF3yz06Edse1wxqzHJZA9TnqY6u0t0gJbxBrmSwXsV1vhRGHRZB7FpH7BNVIZC5w0MFPu5ZBvsoBOSoIvTHX84fKxN6EIZAKAigdnJ8zBZBe3iRLGn85T0oSN1gSwzQJjgvOIgJ3MoUsU',
    })

# user = api.user({'user': 'me'}).get()
# print user.name.data

# user = api.user
# print user.data
# user = user.get()
# print user.data
