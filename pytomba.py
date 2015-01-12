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

        self._api.api_params = api_params

    def __call__(self, *args, **kwargs):
        if 'api_params' in kwargs:
            self._api_params = kwargs['api_params']
            return ApiClient(self._api.__class__(), api_params=self._api_params)

        if 'url_params' in kwargs:
            url = self._api.fill_resource_template_url(self._data, kwargs['url_params'])
            return ApiClient(self._api.__class__(), data=url, api_params=self._api_params)

        if self._current_attr_name == 'data':
            return self._data

        if self._current_attr_name == 'list_nodes':
            if self._data and hasattr(self._data, '__iter__'):
                if isinstance(self._data, list):
                    return []
                return self._data.keys()

            return None

        request_kwargs = self._api.get_request_kwargs(self._api_params)
        request_kwargs.update(kwargs)

        raw = False
        request_method = self._current_attr_name
        if request_method.startswith('raw_'):
            raw = True
            request_method = request_method.replace('raw_', '')

        response_data = requests.request(request_method.upper(), url=self._data, **request_kwargs)
        if not raw:
            response_data = self._api.response_to_native(response_data)

        return ApiClient(self._api.__class__(), data=response_data, api_params=self._api_params)

    def __getattr__(self, name):
        if self._data and (isinstance(self._data, list) or name in self._data) :
            return ApiClient(self._api.__class__(), data=self._data[name], api_params=self._api_params, current_attr_name=name)

        resource_mapping = self._api.resource_mapping
        if name in resource_mapping:
            resource = resource_mapping[name]
            url = self._api.api_root + '/' + resource['resource']
            return ApiClient(self._api.__class__(), data=url, api_params=self._api_params, current_attr_name=name)

        return ApiClient(self._api.__class__(), data=self._data, api_params=self._api_params, current_attr_name=name)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __iter__(self):
        return ApiClientIterator(self._api.__class__(), 
            data=self._data, api_params=self._api_params, 
            current_attr_name=self._current_attr_name)


class ApiClientIterator(ApiClient):

    def __init__(self, *args, **kwargs):
        super(ApiClientIterator, self).__init__(*args, **kwargs)
        self._iterator_index = 0

    def next(self):
        iterator_list = self._api.get_iterator_list(self._data)
        if self._iterator_index >= len(iterator_list):
            next_url = self._api.get_iterator_next_url(self._data)
            if next_url:
                cli = ApiClient(self._api.__class__(), 
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

    def __iter__(self):
        return self


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
