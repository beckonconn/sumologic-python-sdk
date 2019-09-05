import pytest

from sumologic.sumologic import *


def test_sumologic_function_success(requests_mock):
    requests_mock.get('https://api.sumologic.com/api/v1/collectors', [{'status_code': 401}, {'status_code': 301, 'headers': {'Location': 'https://api.us2.sumologic.com/api/v1/collectors'}}])
    requests_mock.get('https://api.us2.sumologic.com/api/v1/collectors', status_code=200)
    s, sumoEnd = sumologic(accessId='1234', accessKey='4567')

    assert isinstance(s, requests.sessions.Session)  # Test returning the Session Object
    assert sumoEnd == 'https://api.sumologic.com/api/v1'  # Test returning the endpoint

def test_endpoint_ssl_error_failure():
    pass

def test_get_endpoint_redirects(requests_mock):
    pass
