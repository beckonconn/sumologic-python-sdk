import pytest

from sumologic.sumologic import *


def test_sumologic_function_success(requests_mock):
    """
    Tests end to end funcitonality including redirects and 401
    to resolve proper endpoint.

    Also tests if the session obj and endpoint are returned when called
    """
    requests_mock.get('https://api.sumologic.com/api/v1/collectors', [{'status_code': 401}, {'status_code': 301, 'headers': {'Location': 'https://api.au.sumologic.com/api/v1/collectors'}}])
    requests_mock.get('https://api.au.sumologic.com/api/v1/collectors', status_code=200)
    s, sumoEnd = sumologic(accessId='1234', accessKey='4567')

    assert isinstance(s, requests.sessions.Session)  # Test returning the Session Object
    assert sumoEnd == 'https://api.au.sumologic.com/api/v1'  # Test returning the endpoint

