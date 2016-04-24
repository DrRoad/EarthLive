'''
Created on 23 Apr 2016

@author: Andy
'''

import logging


class RainfallReading(object):
    '''
    classdocs
    '''
    def __init__(self, data=None, timestamp=None, latitude=None, longitude=None, rainfall=0):
        '''
        Constructor
        '''
        self.metaInfo = {}
        logger = logging.getLogger(__name__)
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.precipitation = rainfall

        if data:
            logger.warn("Loading Domain Object")
            self.timestamp = data.get('timestamp','Missing')
            self.latitude = data.get('latitude','Missing')
            self.longitude = data.get('longitude','Missing')
            self.precipitation = data.get('precipitation',0)
    
    @property
    def key(self):
        keyValues = [self.timestamp,
                    str(self.latitude),
                    str(self.longitude)]
        return '|'.join(keyValues)

    @property
    def value(self):
        return  { 'timestamp' : self.timestamp,
                   'latitude' : self.latitude,
                   'longitude' : self.longitude,
                   'precipitation' : self.precipitation }
 

       
        