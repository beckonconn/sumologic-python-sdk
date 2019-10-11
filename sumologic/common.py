from copy import copy
import json
import logging
import requests

try:
    import cookielib
except ImportError:
    import http.cookiejar as cookielib


def _sumologic_session(accessId, accessKey, endpoint=None, caBundle=None, cookieFile='cookies.txt'):
    session = requests.Session()
    session.auth = (accessId, accessKey)
    session.headers = {'content-type': 'application/json', 'accept': 'application/json'}
    if caBundle is not None:
        session.verify = caBundle
    cj = cookielib.FileCookieJar(cookieFile)
    session.cookies = cj
    if endpoint is None:
        endpoint = _get_endpoint(session)
    if endpoint[-1:] == "/":
        raise Exception("Endpoint should not end with a slash character")

    return session, endpoint


def _get_endpoint(session):
    """
    SumoLogic REST API endpoint changes based on the geo location of the client.
    For example, If the client geolocation is Australia then the REST end point is
    https://api.au.sumologic.com/api/v1

    When the default REST endpoint (https://api.sumologic.com/api/v1) is used the server
    responds with a 401 and causes the SumoLogic class instantiation to fail and this very
    unhelpful message is shown 'Full authentication is required to access this resource'

    This method makes a request to the default REST endpoint and resolves the 401 to learn
    the right endpoint
    """
    endpoint = 'https://api.sumologic.com/api/v1'
    response = session.get('https://api.sumologic.com/api/v1/collectors')  # Dummy call to get endpoint
    if response.status_code == 401:
        response = session.get('https://api.sumologic.com/api/v1/collectors')
        endpoint = response.url.replace('/collectors', '')  # dirty hack to sanitise URI and retain domain
    else:
        endpoint = response.url.replace('/collectors', '')  # dirty hack to sanitise URI and retain domain
    return endpoint
