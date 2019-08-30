import json

from sumologic import SumoLogic


class Collector:
    def __init__(self, accessID, accessKey, uri='/collectors', ):
        if accessID is None and accessKey is None:
            raise TypeError('Missing required arguments: accessID and accessKey')
        self.uri = uri
        self.session, self.endpoint = SumoLogic(accessID, accessKey)


    def search(self, limit=None, offset=None, collectorId=None):
        """
          Method to search for collectors.
          Two different ways:
            1) Search all Collectors using /collectors
            2) Get particular collector by ID using /collectors/$id
        """
        if collectorId is not None:
            """
            REPLACING THIS FROM SUMOLOGIC CLASS
            r = self.get('/collectors/' + str(collector_id))
            return json.loads(r.text), r.headers['etag']
            """
            resp = SumoLogic.get(self, self.uri + '/' + str(collectorId))
            print(resp.text)
            return resp

    def create():
        pass

    def update():
        pass

    def delete():
        pass
