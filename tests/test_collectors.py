import pytest
import requests
import json


from sumologic.collector import Collector

collector = json.dumps({"collector": [{"id": 2}]})

collectors = json.dumps({"collectors": [{"id": 3}, {"id": 4}, {"id": 45}]})


def test_collector_class_init_with_required_args(requests_mock):
    """
    Ensure Class and variables are instantiated correctly
    """
    requests_mock.get('https://api.sumologic.com/api/v1/collectors', text='test')
    endpoint = 'https://api.sumologic.com/api/v1'
    collector = Collector(accessID='12345', accessKey='6789')

    assert isinstance(collector, Collector)
    assert isinstance(collector.sumoSess, requests.sessions.Session)
    assert collector.uri == '/collectors'
    assert collector.endpoint == endpoint


def test_collector_class_init_without_required_args(mocker):
    """
    Ensure an error is provided when 
    the required vars are not provided
    """
    mocker.patch('sumologic.collector.sumologic', side_effect=TypeError('Missing two required args'))
    with pytest.raises(TypeError):
      Collector()


def test_search_with_collectorId(requests_mock):
   """
   Return a single Collector Record and eTag header
   when provided with collector ID
   """
   requests_mock.get('https://api.sumologic.com/api/v1/collectors', text='resp')  # Mocked for session creation
   requests_mock.get('https://api.sumologic.com/api/v1/collectors/2', headers={'ETag': "f58d12c6986f80d6ca25ed8a3943daa9" }, text=collector)
   
   coll = Collector(accessID='12345', accessKey='6789')
   resp, respHead = coll.search(collectorId=2)
 
   assert isinstance(resp, dict) # ensure a dict is returned
   assert resp['collector'][0]['id'] == 2 # all collectors have an ID associated and returned by them
   assert respHead == "f58d12c6986f80d6ca25ed8a3943daa9"


def test_search_without_collectorId(requests_mock):
   """
   Return a list of collectors and make sure it's more than 1
   """
   requests_mock.get('https://api.sumologic.com/api/v1/collectors', [{'text': 'resp'}, {'text': collectors}])  # Mocked for session creation

   coll = Collector(accessID='12345', accessKey='6789')
   resp = coll.search()

   assert isinstance(resp, list)
   assert len(resp) > 1
