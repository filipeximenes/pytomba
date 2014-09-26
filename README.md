# About

Toy project to build a python API client with the following capabilities:
- Easy adaptation to the main API services available on the Web.
- Allow creation of padronized API clients avoiding the need to learn a new library for each service.
- Hypermedia support.
- Pagination support.
- Compatibility with RESTfull services.

## Exceptions

- ApiError
- ApiAuthorizationError
- ApiServerError
- ApiClientError

## Usage:

```
class TwitterApiClient(ApiClient):

    resource_mapping = {
        'statuses_show': {
            'resource': 'statuses/show/{id}',
            'method': 'get',
        },
        'user_timeline': {
            'resource': 'statuses/user_timeline',
            'method': 'get',
        },
        'paginated_user_timeline': {
            'resource': 'statuses/user_timeline',
            'method': 'get_paginated',
        },
        'update_status': {
            'resource': 'statuses/update',
            'method': 'post',
        },
    }


twitter_cli = TwitterApiClient()

for tweet in twitter_cli.user_timeline():
    print tweet

status = twitter_cli.statuses_show({'id': 123456789})

user = status.links.user().follow_link() # follows de link contained in user field

TwitterApiClient.print_docs()
# prints full resource listing with descriptions
```
