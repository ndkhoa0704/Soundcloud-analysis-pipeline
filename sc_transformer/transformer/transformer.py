import pymongo

class Transformer:
    def __init__(self, **kwargs):
        '''
        Transform data from mongodb in batchs
        # Parameters
        - conn_str: connection string
        - dbname: database name
        - interval: interval between each batch processing
        '''
        # Get database
        client = pymongo.MongoClient(kwargs['conn_str'])
        if kwargs['dbname'] == None:
            kwargs['dbname'] = 'scpipe'
        self._db = client.get_database(kwargs['dbname'])
        self._interval = kwargs['intervals']
    
    def transform(self):
        raise NotImplemented