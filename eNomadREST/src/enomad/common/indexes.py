'''
Created on 23 Apr 2016

@author: Andy
'''

INDEX_SEARCH = "search_bin"
INDEX_LOCATION = "location_bin"
SEPARATOR = '|'

class RainfallReadingIndexFactory(object):
    '''
    Index Factory which creates the 2i Indexes for the Rainfall Records
    '''
       
    def buildIndexes(self, rainfallRecord):
        """
        Create the 2i Index Values for a Rainfall Record
        """
        indexes = []
        timestamp = rainfallRecord.timestamp
        latitude = str(rainfallRecord.latitude).replace('.','o')
        longitude = str(rainfallRecord.longitude).replace('.','o')
        indexes[INDEX_SEARCH] = SEPARATOR.join([timestamp, latitude, longitude])
        indexes[INDEX_LOCATION] = SEPARATOR.join(latitude, longitude])
        return indexes
        