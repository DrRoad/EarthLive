'''
Created on 23 Apr 2016

@author: Andy
'''
from contextlib import closing

import logging

import riak
import sys
import traceback
from enomad.common.indexes import RainfallReadingIndexFactory

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
        self.bucket = self.riakClient.bucket(RAINFALL_BUCKET)
        self.indexFactory = RainfallReadingIndexFactory()
        self.logger = logging.getLogger(__name__)
    
    def insertRainfallReading(self, rainfallReading):
        """
        Add a Rainfall Record into the database 
        """
        storedObject = None
        try:
            self.logger.info('Adding Record:' + rainfallReading.key)
            dataObject = self.bucket.new(rainfallReading.key)
            self.logger.info('Got Data Object')
            indexes = self.indexFactory.buildIndexes(rainfallReading)
            dataObject.data = rainfallReading.value
            for idxName, idxValue in indexes.iteritems():
                dataObject.add_index(idxName,str(idxValue))
            self.logger.info('About to Store Data Object')
            storedObject = dataObject.store(return_body=True)
            self.logger.info('Stored Data Object')
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
            with closing(self.riakClient.stream_index(RAINFALL_BUCKET, RainfallReadingIndexFactory.INDEX_SEARCH,
                                             startKey=start + RainfallReadingIndexFactory.SEPARATOR + '~',
                                             endKey=end + RainfallReadingIndexFactory.SEPARATOR + '~',
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
        _,idxLatitude,idxLongitude = term.split(RainfallReadingIndexFactory.SEPARATOR)
        if sqrt(pow(latitude - float(idxLatitude),2) +  pow(latitude - float(idxLatitude),2)) <= allowedVariance:
            return True
        return False

    
