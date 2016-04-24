'''
Created on 23 Apr 2016

@author: Andy
'''

class RainfallReading(object):
    '''
    classdocs
    '''
    def __init__(self, data=None, timestamp=None, latitude=None, longitude=None, rainfall=0):
        '''
        Constructor
        '''
        if data:
            self.metaInfo = data
        else:
            self.metaInfo = {}
            self.timestamp = timestamp
            self.latitude = latitude
            self.longitude = longitude
            self.rainfall = rainfall
    
    @property
    def key(self):
        return '|'.join([self.timestamp,self.latitude,self.longitude])

    @property
    def value(self):
        return self.metaInfo
    
    @property 
    def timestamp(self):
        self.metaInfo.get("timestamp")
        
    @timestamp.setter
    def timestamp(self,value):
        self.metaInfo["timestamp"] = value

    @property
    def latitude(self):
        self.metaInfo.get("latitude")
        
    @latitude.setter
    def latitude(self,value):
        self.metaInfo["latitude"] = value

    @property
    def longitude(self):
        self.metaInfo.get("longitude")
        
    @longitude.setter
    def longitude(self,value):
        self.metaInfo["longitude"] = value
        
    @property
    def rainfall(self):
        self.metaInfo.get("precipitation")
        
    @rainfall.setter
    def rainfall(self,value):
        self.metaInfo["precipitation"] = value
        
        