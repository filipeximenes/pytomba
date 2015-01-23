# coding: utf-8

from requests_oauthlib import OAuth1

from pytomba import ApiClient, BaseClientAdapter


class TwitterClientAdapter(BaseClientAdapter):
    api_root = 'https://api.twitter.com/1.1'
    resource_mapping = {
        'mentions_timeline': {
            'resource': '/statuses/mentions_timeline.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/statuses/user_timeline'
        },
        'statuses_user_timeline': {
            'resource': 'statuses/user_timeline.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/statuses/user_timeline'
        },
        'statuses_home_timeline': {
            'resource': 'statuses/home_timeline.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/statuses/home_timeline'
        },
        'statuses_retweets_of_me': {
            'resource': 'statuses/retweets_of_me.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/statuses/retweets_of_me'
        },
        'statuses_retweets_of_id': {
            'resource': 'statuses/retweets/{id}.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/statuses/retweets/%3Aid'
        },
        'statuses_show': {
            'resource': 'statuses/show.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/statuses/show/%3Aid'
        },
        'statuses_destroy_from_id': {
            'resource': 'statuses/destroy/{id}.json',
            'docs': 'https://dev.twitter.com/rest/reference/post/statuses/destroy/%3Aid'
        },
        'statuses_update': {
            'resource': 'statuses/update.json',
            'docs': 'https://dev.twitter.com/rest/reference/post/statuses/update'
        },
        'statuses_retweet_id': {
            'resource': 'statuses/retweet/{id}.json',
            'docs': 'https://dev.twitter.com/rest/reference/post/statuses/retweet/%3Aid'
        },
        'statuses_oembed': {
            'resource': 'statuses/oembed.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/statuses/oembed'
        },
        'retweeters_of_id': {
            'resource': 'retweeters/ids.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/statuses/retweeters/ids'
        },
        'statuses_lookup': {
            'resource': 'statuses/lookup.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/statuses/lookup'
        },
        'media_upload': {
            'resource': 'media/upload.json',
            'docs': 'https://dev.twitter.com/rest/reference/post/media/upload'
        },
        'direct_messages_sent': {
            'resource': 'direct_messages/sent.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/direct_messages/sent'
        },
        'direct_messages_show': {
            'resource': 'direct_messages/show.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/direct_messages/show'
        },
        'search_tweets': {
            'resource': 'search/tweets.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/search/tweets'
        },
        'direct_messages': {
            'resource': 'direct_messages.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/direct_messages'
        },
        'direct_messages_destroy': {
            'resource': 'direct_messages/destroy.json',
            'docs': 'https://dev.twitter.com/rest/reference/post/direct_messages/destroy'
        },
        'direct_messages_new': {
            'resource': 'direct_messages/new.json',
            'docs': 'https://dev.twitter.com/rest/reference/post/direct_messages/new'
        },
        'friendships_no_retweets_ids': {
            'resource': 'friendships/no_retweets/ids.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/friendships/no_retweets/ids'
        },
        'friends_ids': {
            'resource': 'friends/ids.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/friends/ids'
        },
        'followers_ids': {
            'resource': 'followers/ids.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/followers/ids'
        },
        'friendships_incoming': {
            'resource': 'friendships/incoming.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/friendships/incoming'
        },
        'friendships_outgoing': {
            'resource': 'friendships/outgoing.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/friendships/outgoing'
        },
        'friendships_create': {
            'resource': 'friendships/create.json',
            'docs': 'https://dev.twitter.com/rest/reference/post/friendships/create'
        },
        'friendships_destroy': {
            'resource': 'friendships/destroy.json',
            'docs': 'https://dev.twitter.com/rest/reference/post/friendships/destroy'
        },
        'friendships_update': {
            'resource': 'friendships/update.json',
            'docs': 'https://dev.twitter.com/rest/reference/post/friendships/update'
        },
        'friendships_show': {
            'resource': 'friendships/show.json',
            'docs': 'https://dev.twitter.com/rest/reference/get/friendships/show'
        },
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

# timeline = cli.user_timeline().get(params={'screen_name': 'twitterapi'})

# status = cli.statuses_show({'id': 515109944312733696})
# print(status.user.url())

# timeline = cli.user_timeline.get()
# print timeline[0].text.list_nodes()
# print timeline[0].list_nodes()
