'''
Created on 23 Apr 2016

@author: Andy
'''

import riak

from enomad.common.indexs import RainfallRecordIndexFactory

RAINFALL_BUCKET = 'rainfall'

class RainfallDatabase(object):
    '''
    classdocs
    
    '''
    def __init__(self,riakHost='127.0.0.1', riakPort=8098):
        """
        """
        riakClient = riak.RiakClient(host=riakHost, http_port=riakPort)
        self.bucket = riakClient.bucket(RAINFALL_BUCKET)
        self.indexFactory = RainfallRecordIndexFactory()
    
    def insertRainfallReading(self, rainfallReading):
        """
        """
        try:
            dataObject = self.bucket.new(rainfallReading.key())
            indexes = self.indexFactory.buildIndexes(rainfallReading)
            value = rainfallReading.metaInfo
            dataObject.data = value
            dataObject.indexes = indexes
            storedObject = dataObject.store(return_body=True)
        except Exception, e:
            raise e
        return storedObject
        
    def 
    
