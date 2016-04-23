'''
Created on 23 Apr 2016

@author: Andy
'''

INDEX_SEARCH = "search_bin"
SEPARATOR = '|'

class RainfallReadingIndexFactory(object):
    '''
    classdocs
    '''
       
    def buildIndexes(self, rainfallRecord):
        """
        Create the 2i Index Values for a Rainfall Record
        """
        indexes = []
        timestamp = rainfallRecord.timestamp
        latitude = rainfallRecord.latitude
        longitude = rainfallRecord.longitude
        indexes[INDEX_SEARCH] = SEPARATOR.join([timestamp, latitude, longitude])
        return indexes
        