
## available exceptions

ApiError
ApiAuthorizationError
ApiServerError
ApiClientError

## usage:

```
# class TwitterResponseWrapper(ApiClientResponseWrapper):

    


class TwitterApiClient(ApiClient):
    # response_wrapper_class = TwitterResponseWrapper
    
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

    def _get_request_params(self):
        # ...
        return request

    def _process_response(self, response):
        # process
        # ex.: unwrap response, throw exceptions ...
        return response

    def _paginated(self, seed):
        url = seed
        while url:
            data = self._get(url)

            for bla in data.data:
                yield bla

            url = data.links.next


twitter_cli = TwitterApiClient()

for tweet in twitter_cli.user_timeline():
    print tweet

status = twitter_cli.statuses_show({'id': 123456789})

user = status.links.user().follow_link() # follows de link contained in user field

TwitterApiClient.print_docs()
# prints full resource listing with descriptions
```
