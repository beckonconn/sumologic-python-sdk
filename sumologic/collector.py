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
          Different ways:
            1) Search all Collectors using /collectors
            2) Get particular collector by ID using /collectors/$id
            3) TODO: Add name search
        """
        if collectorId is not None:
            resp = self.sumoSess.get(self.endpoint + self.uri + '/' + str(collectorId))
            return resp.json(), resp.headers['etag']
        elif limit is not None or offset is not None:
            p = {'limit': limit, 'offset': offset}
            resp = self.sumoSess.get(self.endpoint + self.uri, params=p)
            return resp.json()['collectors']
        else:
            resp = self.sumoSess.get(self.endpoint + self.uri)
            return resp.json()['collectors']

    def hosted_collector_create(self, collectorJSON):
        """
        Per documentation, collector creation is only available for hosted collectors.
        Uses POST method
        Things needed:
            1) Header - Doesn't change from application/json
            2) JSON Payload
        Returns: JSON response
        """
        headers = {"Content-Type": "application/json"}
        resp = self.sumoSess.post(self.endpoint + self.uri, data=collectorJSON, headers=headers)
        return resp


    def update():
        pass

    def delete():
        pass

    def offline():
        pass
