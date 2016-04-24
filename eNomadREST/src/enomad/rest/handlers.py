'''
Created on 23 Apr 2016

@author: Andy
'''
import logging
import random
import json
from datetime import date
from tornado.web import RequestHandler
from enomad.dao.database import RainfallDatabase
from enomad.common.domain import RainfallReading
 
class VersionHandler(RequestHandler):
    def get(self):
        response = { 'application': 'eNomad',
                     'version': '1.0.2',
                     'last_build':  date.today().isoformat() }
        self.write(response)

class RainfallHandler(RequestHandler):
    """
    Retrieve the details of the Rainfall Records from the Riak Database
    """

    def get(self, latitude, longitude, start, end, threshold=15):
      """
      Find all of the Rainfall Records that exist between the Start & End Date that
      are close to the given latitude and longitude.
      """
      database = RainfallDatabase()
      latitude = float(latitude.replace('o','.'))
      longitude = float(longitude.replace('o','.'))
      records = database.findRainfallRecords(latitude, longitude, start, finish)
      # Only show records with precipitation > threshold
      response = { "rainfall" : [record for records if record.precipitation >= threshold ]}

      self.write(response)

class UploadRecordHandler(RequestHandler):
    """
    Insert a Rainfall Record into the database
    """
    def post(self):
        """
        Insert record into the database
        """
        logger = logging.getLogger(__name__)
        database = RainfallDatabase()
        contents = self.request.body
        logger.warn('Json:' + contents)
        data = json.loads(contents)
        if not isinstance(data,list):
          rainfallReadings = [data]
        else:
          rainfallReadings = data
        for entry in rainfallReadings:
            entry = { str(k) : v for k, v in entry.iteritems()}
            logger.warn('Data:' + str(entry))
            rainfallReading = RainfallReading(data=entry)
            logger.warn('Reading:' + str(rainfallReading.value))
            database.insertRainfallReading(rainfallReading)

class MockRainfallHandler(RequestHandler):
    """
    Mock implementation of the Request Handler which returns a 
    simulated set of Rainfall Records
    """
    def get(self, latitude, longitude, start, end):
        records = [] 
        for i in xrange(10):
            record = {
                "timestamp": "201604131602",
                "latitude": random.randint(5500800,5501000) / float(100000),
                "longitude": random.randint(-15773,-15500) / float(10000),
                "precipitation": random.randint(0,50)
            }
            records.append(record)

        response = { "rainfall" : [records]}
        self.write(response)
