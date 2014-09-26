# coding: utf-8


# import requests


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

    def __get(self, url, **kwargs):
        # fetch resource
        response_data = {
            'next': 'http://www.vinta.com.br/next',
            'links': [
                {'prop': 'self', 'href': 'http://test.com'}
            ]
        }
        return ApiClient(self.api.__class__(), data=response_data, **self.extra_args)

    def get_resource(self, **kwargs):
        return self.__get(self.api.api_root + '/' + self.resource['resource'], **kwargs)

    def get(self, **kwargs):
        if self.resource:
            return self.get_resource(**kwargs)

    def follow_link(self, link_name=None, **kwargs):
        if not link_name:
            return self.__get(self.data, **kwargs)

        link = self.api.find_link(self.data, link_name)

        if not link:
            return

        return self.__get(link, **kwargs)


class TestApiClient(object):

    api_root = 'http://www.vinta.com.br'

    resource_mapping = {
            'users': {
                'resource': 'users/',
                'methods': ['get'],
            }
        }

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
