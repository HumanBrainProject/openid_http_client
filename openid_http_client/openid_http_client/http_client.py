#   Copyright (c) 2018, EPFL/Human Brain Project PCO
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging

import curlify
from requests import Request
from requests.exceptions import HTTPError

import requests
import json


class HttpClient(object):
    headers = {}

    def __init__(self, endpoint, prefix, auth_client=None, raw=False, alternative_endpoint_writing=None):
        self.logger = logging.getLogger(__name__)
        self.curl_logger = logging.getLogger("curl_{}".format(__name__))
        self.raw = raw
        self._prefix = prefix
        self.auth_client = auth_client
        self.req_session = requests.session()
        self.req_session.headers = {"Content-type": "application/json"}
        self.api_root = '{}/{}'.format(endpoint, prefix)
        self.alternative_endpoint_writing = alternative_endpoint_writing

    def _create_full_url(self, endpoint_url):
        """
        Create complete endpoint
        :param endpoint_url: the path or the url
        :return: the full url
        """
        #We need to make sure, that the request (including the access token) is not directed to an unknown host. We therefore only send it either to the api_root or to the local machine.
        if endpoint_url.startswith(self.api_root) or (self.alternative_endpoint_writing is not None and endpoint_url.startswith(self.alternative_endpoint_writing)):
            full_url = endpoint_url
        else:
            full_url = '{api_root}{endpoint_url}'.format(
                api_root=self.api_root,
                endpoint_url=endpoint_url
            )
        return full_url

    def transform_url_to_defined_endpoint(self, provided_by_nexus):
        provided_by_nexus = provided_by_nexus[
                            provided_by_nexus.find(self._prefix) + len(self._prefix):]
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
            self.logger.debug('returned %s %s', response.status_code, response.content)
            return response.raise_for_status()

    def _request(self, method_name, endpoint_url, data=None, headers=None, can_retry=True):
        """
        Making an http call with a specific method
        In case of an Unauthorized response. The auth client will refresh the token and send the
        request again
        :param method_name:
        :param endpoint_url:
        :param data:
        :param headers:
        :param can_retry:
        :return: the response of the http request
        """
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
        self.curl_logger.debug(curlify.to_curl(response.request))
        try:
            if response.status_code >= 500:
                error = HTTPError()
                error.response = response
                raise error

            elif (response.status_code == 401 or response.status_code == 403) and can_retry:
                self.logger.debug(
                    "ERROR - Refreshing token {} {}: {} {}".format(method_name.upper(),
                                                                   response.status_code, full_url,
                                                                   response))
                if self.auth_client is not None:
                    self.auth_client.refresh_token()
                    return self._request(method_name, endpoint_url, data, original_headers,
                                  can_retry=False)
            elif response.status_code > 403:
                self.logger.debug(
                    "ERROR {} {}: {} {}".format(method_name.upper(), response.status_code, full_url,
                                                response))
            else:
                self.logger.debug(
                    "SUCCESS {} {}: {} {}".format(method_name.upper(), response.status_code,
                                                  full_url, json.dumps(data)))
            return self._handle_response(response)
        except HTTPError as e:
            self.logger.debug('request:%s %s\n%r', method_name, full_url, data)
            self.logger.warning(
                "ERROR {} ({}): {} {} {} {}".format(method_name.upper(), e.response.status_code,
                                                    full_url, json.dumps(data), e.response.content,
                                                    e.response.text))
            raise (e)

    def _direct_request(self, method_name, full_url, data=None, headers=None):
        self.logger.debug('%s %s\n%r', method_name, full_url, data)
        method = getattr(requests, method_name)
        headers = headers or {}
        headers.update(headers)
        self.logger.debug('request:%s %s\n%r', method_name, full_url, data)
        response = method(full_url, str(data), headers=headers)
        self.logger.debug('returned %s', response.status_code)
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
