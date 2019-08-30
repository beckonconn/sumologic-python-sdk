import pytest


from sumologic.collector import Collector

@pytest.fixture
def mocked_one_collector_response():
    """
    Creates Dummy Data for testing API responses
    """
    collectors = {
              "id": "2",
              "name": "OtherCollector",
              "collectorType": "Installable",
              "alive": "true",
              "links": [
                 {
                    "rel": "sources",
                    "href": "/v1/collectors/2/sources"
                 }
              ],
              "collectorVersion": "19.33-28",
              "ephemeral": "false",
              "description": "Local Windows Collection",
              "osName": "Windows 7",
              "osArch": "amd64",
              "osVersion": "6.1",
              "category": "local"
           }

    return collectors


# Ensure a class is created when everything is provided correctly
def test_collector_class_init_with_required_args(mocker):
    endpoint = 'https://randomapi.com'
    mock_sl = mocker.patch('sumologic.collector.SumoLogic')
    mock_sl.return_value = mocker.sentinel.SessionObject, endpoint
    collector = Collector(accessID='12345', accessKey='6789')

    assert isinstance(collector, Collector)
    assert collector.uri == '/collectors'
    mock_sl.assert_called_once_with('12345', '6789')
    assert collector.endpoint == endpoint
    assert collector.session is mocker.sentinel.SessionObject

# Ensure an error is provided when the required vars are not provided 
def test_collector_class_init_without_required_args(mocker):
     mock_sl = mocker.patch('sumologic.collector.SumoLogic', side_effect=TypeError('Missing two required args'))
     with pytest.raises(TypeError):
        Collector()


def test_search_with_collectorId(requests_mock, mocked_one_collector_response):
    # mocker.patch('sumologic.collector.SumoLogic', side_effect=mocked_one_collector_response)
    requests_mock.register_uri('GET', '/collectors', text='resp')

    collectorID = 2
    searchCollectors = Collector().search(collectorId=collectorID)
    print(searchCollectors)
    assert 0
