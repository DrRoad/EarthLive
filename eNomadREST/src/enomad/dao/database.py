'''
Created on 23 Apr 2016

@author: Andy
'''
from contextlib import closing

import riak
import sys
import traceback
from enomad.common.indexes import RainfallRecordIndexFactory

RAINFALL_BUCKET = 'rainfall'

class RainfallDatabase(object):
    '''
    Connection to the Riak Database

    Stores the Rainfall records and performs the query to retrieve records
    
    '''
    def __init__(self, riakHost='127.0.0.1', riakPort=8098):
        """
        """
        self.riakClient = riak.RiakClient(host=riakHost, http_port=riakPort)
        self.bucket = riakClient.bucket(RAINFALL_BUCKET)
        self.indexFactory = RainfallRecordIndexFactory()
    
    def insertRainfallReading(self, rainfallReading):
        """
        Add a Rainfall Record into the database 
        """
        try:
            dataObject = self.bucket.new(rainfallReading.key())
            indexes = self.indexFactory.buildIndexes(rainfallReading)
            value = rainfallReading.metaInfo
            dataObject.data = value
            dataObject.indexes = indexes
            storedObject = dataObject.store(return_body=True)
        except Exception, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            raise e
        return storedObject
        
    def findRainfallRecords(self, latitude, longitude, start, finish):
        """
        Find all rainfall records between the start and finish dates which are close to the
        given latitude & longitude
        """
        records = []
        try:
            # Using contextlib.closing
            with closing(self.riakClient.stream_index(RAINFALL_BUCKET, RainfallRecordIndexFactory.INDEX_SEARCH,
                                             startKey=start + RainfallRecordIndexFactory.SEPARATOR + '~',
                                             endKey=end + RainfallRecordIndexFactory.SEPARATOR + '~',
                                             return_terms=True,
                                             max_results=5000,
                                             timeout=20000)) as index:
                for key,term in index:
                    if self.locationFilter(term, latitude, longitude):
                        databaseObject = self.bucket.get(key)
                        record = json.loads(databaseObject.data)
                        records.add(record)

        except Exception, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            raise e

        return records

    def locationFilter(term, latitude, longitude, allowedVariance=2.0):
        """
        Check if the record is close to the given latitude and longitude
        Uses an approximate circle around the requested location.
        """
        _,idxLatitude,idxLongitude = term.split(RainfallRecordIndexFactory.SEPARATOR)
        if sqrt(pow(latitude - float(idxLatitude),2) +  pow(latitude - float(idxLatitude),2)) <= allowedVariance:
            return True
        return False

    
