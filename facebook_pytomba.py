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

    def response_to_native(self, response):
        return response.json()


FacebookApiClient = ApiClient(FacebookClientAdapter())


api = FacebookApiClient({
        'client_id': '1495124414107995',
        'access_token': 'CAAVPzseZAEVsBAPvhGgyeDNkYi5MjnezyZBZATYvSD5hPXZAySvhniEcjhStUWp5rjWfNLsAeOJJYbykR8yZA55fS3IY9nWN6vh9QDNZCgD0hmvnE6ezeWZBu3JdfxNnLOgYrJiI8fiIcAJ2f6ZA8XZCzUvWNNPg1ZBHpJsyrUOWtgXsToGz2GLPWzhNZCLQGOrjZA8nBrZALdyKJVTUnI0lAERrU',
    })

print api.user({'user': 'me'}).list_nodes()

