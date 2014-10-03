# coding: utf-8

import requests


class ApiClient(object):

    def __init__(self, api, resource=None, data=None, extra_args={}, *args, **kwargs):
        self.api = api
        self.resource = resource
        self.data = data
        self.extra_args = extra_args

        self.api.extra_args = extra_args

    def __call__(self, *args, **kwargs):
        if self.data is not None:
            if not args:
                url_params = {}
            else:
                url_params = args[0]
            url = self.api.fill_resource_template_url(self.data, url_params)
            return ApiClient(self.api.__class__(), data=url, extra_args=self.extra_args)

        if args:
            self.extra_args = args[0]
        return ApiClient(self.api.__class__(), extra_args=self.extra_args)

    def __getattr__(self, name):
        if self.data is not None:
            return ApiClient(self.api.__class__(), data=self.data[name], extra_args=self.extra_args)

        resource_mapping = self.api.resource_mapping
        if name in resource_mapping:
            resource = resource_mapping[name]
            url = self.api.api_root + '/' + resource['resource']
            return ApiClient(self.api.__class__(), data=url, extra_args=self.extra_args)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def list_nodes(self):
        if self.data:
            if isinstance(self.data, list):
                return []

            return [key for key, value in self.data.items()]

    def make_request(self, method, url, **kwargs):
        request_kwargs = self.api.get_request_kwargs()
        request_kwargs.update(kwargs)

        self.response = requests.request(method, url=url, **request_kwargs)
        response_data = self.api.response_to_native(self.response)

        return ApiClient(self.api.__class__(), data=response_data, extra_args=self.extra_args)

    def get(self, url_params={}, **kwargs):
        url = self.data
        return self.make_request('GET', url, **kwargs)

    def post(self, url_params={}, **kwargs):
        url = self.data
        return self.make_request('POST', url, **kwargs)

    def put(self, url_params={}, **kwargs):
        url = self.data
        return self.make_request('PUT', url, **kwargs)

    def patch(self, url_params={}, **kwargs):
        url = self.data
        return self.make_request('PATCH', url, **kwargs)

    def delete(self, url_params={}, **kwargs):
        url = self.data
        return self.make_request('DELETE', url, **kwargs)

    def head(self, url_params={}, **kwargs):
        url = self.data
        return self.make_request('HEAD', url, **kwargs)

    def options(self, url_params={}, **kwargs):
        url = self.data
        return self.make_request('OPTIONS', url, **kwargs)

    def follow_link(self, link_name=None, **kwargs):
        if not link_name:
            return self.get(**kwargs)

        link = self.api.find_link(self.data, link_name)

        if not link:
            return

        return self.make_request('GET', link, **kwargs)


class BaseClientAdapter(object):

    def fill_resource_template_url(self, template, params):
        return template.format(**params)

    def get_request_kwargs(self):
        return {}

    def response_to_native(self, response):
        return response.json()

    def find_link(self, data, link_name):
        raise NotImplementedError
