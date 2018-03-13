import logging

import curlify
from requests import Request
from requests.exceptions import HTTPError

import requests
import json

LOGGER = logging.getLogger(__package__)
CURL_LOGGER = logging.getLogger("curl")

class HttpClient(object):

    headers = {}

    def __init__(self, endpoint, prefix, auth_client=None, raw=False):
        self.raw = raw
        self._prefix = prefix
        self.auth_client = auth_client
        self.req_session = requests.session()
        self.req_session.headers = {"Content-type": "application/json"}
        self.api_root = '{}/{}'.format(endpoint, prefix)

    def _create_full_url(self, endpoint_url):
        if endpoint_url.startswith(self.api_root):
            full_url = endpoint_url
        else:
            full_url = '{api_root}{endpoint_url}'.format(
                api_root=self.api_root,
                endpoint_url=endpoint_url
            )
        return full_url

    def transform_url_to_defined_endpoint(self, provided_by_nexus):
        provided_by_nexus = provided_by_nexus[provided_by_nexus.find(self._prefix)+len(self._prefix):]
        return self._create_full_url(provided_by_nexus)

    def _handle_response(self, response):
        if response.status_code == 404:
            return None
        elif response.status_code < 300:
            if self.raw:
                return response
            else:
                return response.json()
        else:
            LOGGER.debug('returned %s %s', response.status_code, response.content)
            return response.raise_for_status()

    def _request(self, method_name, endpoint_url, data=None, headers=None, can_retry=True):
        if endpoint_url.startswith('http'):
            endpoint_url = self.transform_url_to_defined_endpoint(endpoint_url)
        full_url = self._create_full_url(endpoint_url)
        if type(data) is dict or type(data) is list:
            data = json.dumps(data)
        original_headers = headers
        headers = headers or {}
        if self.auth_client is not None:
            headers.update(self.auth_client.get_headers())
        req = Request(method_name, full_url, data=data, headers=headers)
        prepped_request = self.req_session.prepare_request(req)
        response = self.req_session.send(prepped_request, timeout=30)
        CURL_LOGGER.info(curlify.to_curl(response.request))
        try:
            if response.status_code >= 500:
                error = HTTPError()
                error.response = response
                raise error
            elif response.status_code > 401:
                LOGGER.error("ERROR {} {}: {} {}".format(method_name.upper(),response.status_code,  full_url, response))
            elif response.status_code == 401 and can_retry:
                LOGGER.error(
                    "ERROR - Refreshing token {} {}: {} {}".format(method_name.upper(), response.status_code, full_url,
                                                response))
                if self.auth_client is not None:
                    self.auth_client.refresh_token()
                    self._request(method_name, endpoint_url, data, original_headers, can_retry=False)
            else:
                LOGGER.debug("SUCCESS {} {}: {} {}".format(method_name.upper(), response.status_code, full_url, json.dumps(data)))
            return self._handle_response(response)
        except HTTPError as e:
            LOGGER.debug('request:%s %s\n%r', method_name, full_url, data)
            LOGGER.error("ERROR {} ({}): {} {} {} {}".format(method_name.upper(), e.response.status_code, full_url, json.dumps(data), e.response.content, e.response.text))
            raise(e)

    @staticmethod
    def _direct_request(method_name, full_url, data=None, headers=None):
        LOGGER.debug('%s %s\n%r', method_name, full_url, data)
        method = getattr(requests, method_name)
        headers = headers or {}
        headers.update(headers)
        LOGGER.debug('request:%s %s\n%r', method_name, full_url, data)
        response = method(full_url, str(data), headers=headers)
        LOGGER.debug('returned %s', response.status_code)
        return response

    def put(self, *args, **kwargs):
        return self._request('put', *args, **kwargs)

    def get(self, *args, **kwargs):
        # return NexusPayload(response.content)?
        return self._request('get', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request('post', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._request('patch', *args, **kwargs)

    def delete(self, endpoint_url):
        return self._request('delete', endpoint_url)
