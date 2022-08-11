from platform import python_implementation
import pandas as pd
import numpy as np
from datetime import date
import json
import pymongo
import time

class Transformer:
    def __init__(self, conn_str: str, dbname: str, interval: int):
        '''
        Transform data from mongodb in each interval
        # Parameters
        - conn_str: connection string
        - dbname: database name
        - interval: interval between each batch processing
        '''
        # Get database
        client = pymongo.MongoClient(conn_str)
        self._db = client.get_database('scpipe')
    
    def transform(self):
        raise NotImplemented

class SoundCloud_Transformer(Transformer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        