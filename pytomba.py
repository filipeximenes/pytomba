# coding: utf-8

import requests
import webbrowser


class ApiClient(object):

    def __init__(self, api, data=None, request_kwargs=None, api_params={}, 
            resource=None, *args, **kwargs):
        self._api = api
        self._data = data
        self._api_params = api_params
        self._request_kwargs = request_kwargs
        self._resource = resource

    def __call__(self, *args, **kwargs):
        if 'api_params' in kwargs:
            self._api_params = kwargs['api_params']
            return ApiClient(self._api.__class__(), data=self._data, api_params=self._api_params)

        if 'url_params' in kwargs:
            url = self._api.fill_resource_template_url(self._data, kwargs['url_params'])
            return ApiClientExecutor(self._api.__class__(), data=url, api_params=self._api_params)

        return ApiClientExecutor(self._api.__class__(), data=self._data, api_params=self._api_params,
            resource=self._resource)

    def __getattr__(self, name):
        if self._data and \
            ((isinstance(self._data, list) and isinstance(name, int)) or \
                (hasattr(self._data, '__iter__') and name in self._data)):
            return ApiClient(self._api.__class__(), data=self._data[name], api_params=self._api_params)

        resource_mapping = self._api.resource_mapping
        if name in resource_mapping:
            resource = resource_mapping[name]
            url = self._api.api_root + '/' + resource['resource']
            return ApiClient(self._api.__class__(), data=url, api_params=self._api_params, 
                resource=resource)

        raise KeyError(name)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __iter__(self):
        return ApiClientExecutor(self._api.__class__(), 
            data=self._data, request_kwargs=self._request_kwargs, api_params=self._api_params)

    def __dir__(self):
        if self._api and self._data == None:
            return [key for key in self._api.resource_mapping.keys()]

        if isinstance(self._data, dict):
            return self._data.keys()

        return []


class ApiClientExecutor(ApiClient):

    def __init__(self, api, *args, **kwargs):
        super(ApiClientExecutor, self).__init__(api, *args, **kwargs)
        self._iterator_index = 0

    def __call__(self, *args, **kwargs):
        return object.__call__(*args, **kwargs)

    def __getattr__(self, name):
        return object.__getattr__(name)

    def __getitem__(self, key):
        return object.__getitem__(name)

    def __iter__(self):
        return self

    def data(self):
        return self._data

    def _make_request(self, request_method, raw=False, *args, **kwargs):
        request_kwargs = self._api.get_request_kwargs(self._api_params)
        request_kwargs.update(kwargs)

        if not 'url' in request_kwargs:
            request_kwargs['url'] = self._data

        response = requests.request(request_method, **request_kwargs)
        if not raw:
            response = self._api.response_to_native(response)

        return ApiClient(self._api.__class__(), data=response, 
            request_kwargs=request_kwargs, api_params=self._api_params)

    def get(self, *args, **kwargs):
        return self._make_request('GET', *args, **kwargs)

    def raw_get(self, *args, **kwargs):
        return self._make_request('GET', raw=True, *args, **kwargs)

    def next(self):
        iterator_list = self._api.get_iterator_list(self._data)
        if self._iterator_index >= len(iterator_list):
            new_request_kwargs = self._api.get_iterator_next_request_kwargs(
                self._request_kwargs, self._data)

            if new_request_kwargs:
                cli = ApiClientExecutor(self._api.__class__(), api_params=self._api_params)
                response = cli.get(**new_request_kwargs)
                self._data = response._data
                self._iterator_index = 0
            else:
                raise StopIteration()

        item = iterator_list[self._iterator_index]
        self._iterator_index += 1

        return ApiClient(self._api.__class__(), data=item, api_params=self._api_params)

    def open_docs(self):
        if not self._resource:
            raise KeyError()
            
        new = 2 # open in new tab
        webbrowser.open(self._resource['docs'], new=new)

    def open_in_browser(self):
        new = 2 # open in new tab
        webbrowser.open(self._data, new=new)        



class BaseClientAdapter(object):

    def fill_resource_template_url(self, template, params):
        return template.format(**params)

    def response_to_native(self, response):
        return response.json()

    def get_request_kwargs(self):
        return {}

    def get_iterator_list(self, response_data):
        raise NotImplementedError()

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs, response_data):
        raise NotImplementedError()
