# coding: utf-8

import requests


class ApiClient(object):

    def __init__(self, api, resource=None, data=None, extra_args={}, *args, **kwargs):
        self._api = api
        self._resource = resource
        self._data = data
        self._extra_args = extra_args

        self._api.extra_args = extra_args

    def __call__(self, *args, **kwargs):
        if self._data is not None:
            if not args:
                url_params = {}
            else:
                url_params = args[0]
            url = self._api.fill_resource_template_url(self._data, url_params)
            return ApiClient(self._api.__class__(), data=url, extra_args=self._extra_args)

        if args:
            self._extra_args = args[0]
        return ApiClient(self._api.__class__(), extra_args=self._extra_args)

    def __getattr__(self, name):
        if self._data is not None:
            return ApiClient(self._api.__class__(), data=self._data[name], extra_args=self._extra_args)

        resource_mapping = self._api.resource_mapping
        if name in resource_mapping:
            resource = resource_mapping[name]
            url = self._api.api_root + '/' + resource['resource']
            return ApiClient(self._api.__class__(), data=url, extra_args=self._extra_args)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def data(self):
        return self._data

    def list_nodes(self):
        if self._data and hasattr(self._data, '__iter__'):
            if isinstance(self._data, list):
                return []
            return self._data.keys()

        return None

    def _make_request(self, method, url, **kwargs):
        request_kwargs = self._api.get_request_kwargs()
        request_kwargs.update(kwargs)

        self.response = requests.request(method, url=url, **request_kwargs)
        response_data = self._api.response_to_native(self.response)

        return ApiClient(self._api.__class__(), data=response_data, extra_args=self._extra_args)

    def get(self, url_params={}, **kwargs):
        url = self._data
        return self._make_request('GET', url, **kwargs)

    def post(self, url_params={}, **kwargs):
        url = self._data
        return self._make_request('POST', url, **kwargs)

    def put(self, url_params={}, **kwargs):
        url = self._data
        return self._make_request('PUT', url, **kwargs)

    def patch(self, url_params={}, **kwargs):
        url = self._data
        return self._make_request('PATCH', url, **kwargs)

    def delete(self, url_params={}, **kwargs):
        url = self._data
        return self._make_request('DELETE', url, **kwargs)

    def head(self, url_params={}, **kwargs):
        url = self._data
        return self._make_request('HEAD', url, **kwargs)

    def options(self, url_params={}, **kwargs):
        url = self._data
        return self._make_request('OPTIONS', url, **kwargs)


class BaseClientAdapter(object):

    def fill_resource_template_url(self, template, params):
        return template.format(**params)

    def get_request_kwargs(self):
        return {}

    def response_to_native(self, response):
        return response.json()

    def find_link(self, data, link_name):
        raise NotImplementedError
