import json

import sumologic.sumologic as sumologic


class Collector(object):
    def __init__(self, accessID, accessKey, caBundle=None, uri='/collectors'):

        # need to make sure minimum req args are passed
        if accessID is None and accessKey is None:
            raise TypeError('Missing required arguments: accessID and accessKey')

        # set session and endpoint
        self.sumoSess, self.endpoint = sumologic(accessID, accessKey, caBundle=caBundle)

        # set other class vars
        self.uri = uri

    def search(self, limit=None, offset=None, collectorId=None):
        """
          Method to search for collectors.
          Two different ways:
            1) Search all Collectors using /collectors
            2) Get particular collector by ID using /collectors/$id
        """
        if collectorId is not None:
            resp = self.sumoSess.get(self.endpoint + self.uri + '/' + str(collectorId))
            return resp.json(), resp.headers['etag']
        else:
            resp = self.sumoSess.get(self.endpoint + self.uri)
            return resp.json()['collectors']




    def create():
        pass

    def update():
        pass

    def delete():
        pass
