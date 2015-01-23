# coding: utf-8

from requests_oauthlib import OAuth2

from pytomba import ApiClient, BaseClientAdapter


class FacebookClientAdapter(BaseClientAdapter):
    api_root = 'https://graph.facebook.com/v2.2'
    resource_mapping = {
        'object': {
            'resource': '{id}',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2'
        },
        'user_accounts': {
            'resource': '{id}/accounts',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/accounts'
        },
        'user_achievements': {
            'resource': '{id}/achievements',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/achievements'
        },
        'user_activities': {
            'resource': '{id}/activities',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/activities'
        },
        'user_albums': {
            'resource': '{id}/albums',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/albums'
        },
        'user_applications_developer': {
            'resource': '{id}/applications/developer',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/applications/developer'
        },
        'user_apprequests': {
            'resource': '{id}/apprequests',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/apprequests'
        },
        'user_books': {
            'resource': '{id}/books',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/books'
        },
        'user_events': {
            'resource': '{id}/events',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/events'
        },
        'user_family': {
            'resource': '{id}/family',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/family'
        },
        'user_feed': {
            'resource': '{id}/feed',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/feed'
        },
        'user_friendlists': {
            'resource': '{id}/friendlists',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/friendlists'
        },
        'user_friends': {
            'resource': '{id}/friends',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/friends'
        },
        'user_games': {
            'resource': '{id}/games',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/games'
        },
        'user_groups': {
            'resource': '{id}/groups',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/groups'
        },
        'user_home': {
            'resource': '{id}/home',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/home'
        },
        'user_ids_for_business': {
            'resource': '{id}/ids_for_business',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/ids_for_business'
        },
        'user_inbox': {
            'resource': '{id}/inbox',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/inbox'
        },
        'user_interests': {
            'resource': '{id}/interests',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/interests'
        },
        'user_invitable_friends': {
            'resource': '{id}/invitable_friends',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/invitable_friends'
        },
        'user_likes': {
            'resource': '{id}/likes',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/likes'
        },
        'user_music': {
            'resource': '{id}/music',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/music'
        },
        'user_notifications': {
            'resource': '{id}/notifications',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/notifications'
        },
        'user_outbox': {
            'resource': '{id}/outbox',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/outbox'
        },
        'user_payment_transactions': {
            'resource': '{id}/payment_transactions',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/payment_transactions'
        },
        'user_permissions': {
            'resource': '{id}/permissions',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/permissions'
        },
        'user_photos': {
            'resource': '{id}/photos',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/photos'
        },
        'user_picture': {
            'resource': '{id}/picture',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/picture'
        },
        'user_pokes': {
            'resource': '{id}/pokes',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/pokes'
        },
        'user_scores': {
            'resource': '{id}/scores',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/scores'
        },
        'user_taggable_friends': {
            'resource': '{id}/taggable_friends',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/taggable_friends'
        },
        'user_tagged_places': {
            'resource': '{id}/tagged_places',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/tagged_places'
        },
        'user_television': {
            'resource': '{id}/television',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/television'
        },
        'user_videos': {
            'resource': '{id}/videos',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/videos'
        },
        'user_videos_uploaded': {
            'resource': '{id}/videos/uploaded',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/user/videos'
        },
        'page_albums': {
            'resource': '{id}/albums',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/albums'
        },
        'page_blocked': {
            'resource': '{id}/blocked',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/blocked'
        },
        'page_conversations': {
            'resource': '{id}/conversations',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/conversations'
        },
        'page_events': {
            'resource': '{id}/events',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/events'
        },
        'page_feed': {
            'resource': '{id}/feed',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/feed'
        },
        'page_global_brand_children': {
            'resource': '{id}/global_brand_children',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/global_brand_children'
        },
        'page_insights': {
            'resource': '{id}/insights',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/insights'
        },
        'page_links': {
            'resource': '{id}/links',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/links'
        },
        'page_locations': {
            'resource': '{id}/locations',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/locations'
        },
        'page_milestones': {
            'resource': '{id}/milestones',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/milestones'
        },
        'page_offers': {
            'resource': '{id}/offers',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/offers'
        },
        'page_photos': {
            'resource': '{id}/photos',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/photos'
        },
        'page_picture': {
            'resource': '{id}/picture',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/picture'
        },
        'page_ratings': {
            'resource': '{id}/ratings',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/ratings'
        },
        'page_settings': {
            'resource': '{id}/settings',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/settings'
        },
        'page_statuses': {
            'resource': '{id}/statuses',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/statuses'
        },
        'page_tabs': {
            'resource': '{id}/tabs',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/tabs'
        },
        'page_videos': {
            'resource': '{id}/videos',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/videos'
        },
        'page_': {
            'resource': '{id}/',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/page/'
        },
        'debug_token': {
            'resource': 'debug_token',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/debug_token'
        },
        'object_comments': {
            'resource': '{id}/comments',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/object/comments'
        },
        'object_likes': {
            'resource': '{id}/likes',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/object/likes'
        },
        'object_sharedposts': {
            'resource': '{id}/sharedposts',
            'docs': 'https://developers.facebook.com/docs/graph-api/reference/v2.2/object/sharedposts'
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

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs, response_data):
        paging = response_data.get('paging')
        if not paging:
            return
        url = paging.get('next')

        if url:
            return {'url': url}


FacebookApiClient = ApiClient(FacebookClientAdapter())

from decouple import config


api = FacebookApiClient(api_params={
        'client_id': config('FACEBOOK_CLIENT_ID'),
        'access_token': config('FACEBOOK_ACCESS_TOKEN'),
    })

# user_likes = api.user_likes(url_params={'user': 'me'}).get()

# print user_likes.data

# for item in user_likes:
#     print item.name.data()


# print user.data
# print user.name.data

# user = api.user
# print user.data
# user = user.get()
# print user.data
