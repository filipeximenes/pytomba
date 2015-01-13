# coding: utf-8

import requests


class ApiClient(object):

    def __init__(self, api, resource=None, data=None, api_params={}, 
        current_attr_name=None, *args, **kwargs):
        self._api = api
        self._resource = resource
        self._data = data
        self._api_params = api_params
        self._current_attr_name = current_attr_name

    def __call__(self, *args, **kwargs):
        if 'api_params' in kwargs:
            self._api_params = kwargs['api_params']
            return ApiClient(self._api.__class__(), api_params=self._api_params)

        if 'url_params' in kwargs:
            url = self._api.fill_resource_template_url(self._data, kwargs['url_params'])
            return ApiClientExecutor(self._api.__class__(), data=url, api_params=self._api_params)

        return ApiClientExecutor(self._api.__class__(), data=self._data, 
            api_params=self._api_params, current_attr_name=self._current_attr_name)

    def __getattr__(self, name):
        if self._data and \
            ((isinstance(self._data, list) and isinstance(name, int)) or \
                (hasattr(self._data, '__iter__') and name in self._data)):
            return ApiClient(self._api.__class__(), data=self._data[name], api_params=self._api_params, current_attr_name=name)

        resource_mapping = self._api.resource_mapping
        if name in resource_mapping:
            resource = resource_mapping[name]
            url = self._api.api_root + '/' + resource['resource']
            return ApiClient(self._api.__class__(), data=url, api_params=self._api_params, current_attr_name=name)

        raise KeyError(name)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __iter__(self):
        return ApiClientIterator(self._api.__class__(), 
            data=self._data, api_params=self._api_params, 
            current_attr_name=self._current_attr_name)


class ApiClientExecutor(ApiClient):

    def __init__(self, *args, **kwargs):
        super(ApiClientExecutor, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return object.__call__(*args, **kwargs)

    def __getattr__(self, name):
        return object.__getattr__(name)

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return object.__iter__()

    def data(self):
        return self._data

    def list_nodes(self):
        if self._data and hasattr(self._data, '__iter__'):
            if isinstance(self._data, list):
                return []
            return self._data.keys()

        return None

    def _make_request(self, request_method, raw=False, *args, **kwargs):
        request_kwargs = self._api.get_request_kwargs(self._api_params)
        request_kwargs.update(kwargs)

        response_data = requests.request(request_method, url=self._data, **request_kwargs)
        if not raw:
            response_data = self._api.response_to_native(response_data)

        return ApiClient(self._api.__class__(), data=response_data, api_params=self._api_params)

    def get(self, *args, **kwargs):
        return self._make_request('GET', *args, **kwargs)

    def raw_get(self, *args, **kwargs):
        return self._make_request('GET', raw=True, *args, **kwargs)


class ApiClientIterator(ApiClient):

    def __init__(self, *args, **kwargs):
        super(ApiClientIterator, self).__init__(*args, **kwargs)
        self._iterator_index = 0

    def __call__(self, *args, **kwargs):
        return object.__call__(*args, **kwargs)

    def __getattr__(self, name):
        return object.__getattr__(name)

    def __getitem__(self, key):
        return object.__getitem__(key)

    def __iter__(self):
        return self

    def next(self):
        iterator_list = self._api.get_iterator_list(self._data)
        if self._iterator_index >= len(iterator_list):
            next_url = self._api.get_iterator_next_url(self._data)
            if next_url:
                cli = ApiClientExecutor(self._api.__class__(), 
                    data=next_url, 
                    api_params=self._api_params)
                response = cli.get()
                self._data = response._data
                self._iterator_index = 0
            else:
                raise StopIteration()

        item = iterator_list[self._iterator_index]
        self._iterator_index += 1

        return ApiClient(self._api.__class__(), 
            data=item, 
            api_params=self._api_params, 
            current_attr_name=self._iterator_index)


class BaseClientAdapter(object):

    def fill_resource_template_url(self, template, params):
        return template.format(**params)

    def response_to_native(self, response):
        return response.json()

    def get_request_kwargs(self):
        return {}

    def get_iterator_list(self, response_data):
        raise NotImplementedError()

    def get_iterator_next_url(self, response_data):
        raise NotImplementedError()
