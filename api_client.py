# coding: utf-8


import requests


class ApiClient(object):

    def __init__(self, api, resource=None, data=None, **kwargs):
        self.api = api
        self.resource = resource
        self.data = data
        self.extra_args = kwargs

    def __call__(self, *args, **kwargs):
        if self.resource:
            return self.get_resource(**kwargs)

        if self.data:
            return self.data

        return ApiClient(self.api.__class__(), **self.extra_args)

    def __getattr__(self, name):
        if self.resource:
            return self.get_resource()

        if self.data:
            return  ApiClient(self.api.__class__(), data=self.data[name], **self.extra_args)

        resource_mapping = self.api.resource_mapping
        if name in resource_mapping:
            self.resource = resource_mapping[name]
            return self.get_resource()

    def make_request(self, method, url, **kwargs):
        self.response = requests.request(method, url, **kwargs)
        response_data = self.api.process_response(self.response)

        return ApiClient(self.api.__class__(), data=response_data, **self.extra_args)

    def get_request_url(self):
        if self.resource:
            return self.api.api_root + '/' + self.resource['resource']

        if self.data:
            return self.data

    def get_resource(self, **kwargs):
        url = self.get_request_url()
        return self.make_request('GET', url, **kwargs)

    def get(self, **kwargs):
        url = self.get_request_url()
        return self.make_request('GET', url, **kwargs)

    def post(self, **kwargs):
        url = self.get_request_url()
        return self.make_request('POST', url, **kwargs)

    def put(self, **kwargs):
        url = self.get_request_url()
        return self.make_request('PUT', url, **kwargs)

    def patch(self, **kwargs):
        url = self.get_request_url()
        return self.make_request('PATCH', url, **kwargs)

    def delete(self, **kwargs):
        url = self.get_request_url()
        return self.make_request('DELETE', url, **kwargs)

    def head(self, **kwargs):
        url = self.get_request_url()
        return self.make_request('HEAD', url, **kwargs)

    def options(self, **kwargs):
        url = self.get_request_url()
        return self.make_request('OPTIONS', url, **kwargs)

    def follow_link(self, link_name=None, **kwargs):
        if not link_name:
            return self.get(**kwargs)

        link = self.api.find_link(self.data, link_name)

        if not link:
            return

        return self.make_request('GET', link, **kwargs)


class TestApiClient(object):

    api_root = 'http://www.vinta.com.br'

    resource_mapping = {
            'users': {
                'resource': 'users/',
                'methods': ['get'],
            }
        }

    def process_response(self, response):
        return response.json()

    def find_link(self, data, link_name):
        for link in data['links']:
            if link['prop'] == link_name:
                return link['href']


Cli = ApiClient(TestApiClient())

cli = Cli()

print cli.users
print cli.users()
print cli.users.follow_link('self')
print cli.users.next.follow_link()
