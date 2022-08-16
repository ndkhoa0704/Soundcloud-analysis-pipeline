import pymongo

class Collector:
    '''
    An abstract class for all crawlers, scrapers for the project
    '''
    def __init__(self, **kwargs):
        '''
        Get data from internet
        # Parameters
        - conn_str: connection string
        - dbname: database name
        - interval: interval between each batch processing
        '''

        # Get data
        client = pymongo.MongoClient(kwargs['conn_str'])
        if kwargs['dbname'] == None:
            kwargs['dbname'] = 'scpipe'
        self._db = client.get_database(kwargs['dbname'])

    def collect(self):
        raise NotImplemented