'''
Created on 23 Apr 2016

@author: Andy
'''

import random
import json
from datetime import date
from tornado.web import RequestHandler
from enomad.dao.database import RainfallDatabase
 
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

    def __init__(self):

      self.database = RainfallDatabase()

    def get(self, latitude, longitude, start, end):
      """
      Find all of the Rainfall Records that exist between the Start & End Date that
      are close to the given latitude and longitude.
      """
      latitude = float(latitude.replace('o','.'))
      longitude = float(longitude.replace('o','.'))
      records = self.database.findRainfallRecords(latitude, longitude, start, finish)

      response = { "rainfall" : records }

      self.write(response)

class UploadRecordHandler(RequestHandler):
  """
  Insert a Rainfall Record into the database
  """
    def __init__(self):
      self.database = RainfallDatabase()

    def post(self):
        """
        Insert record into the database
        """
        data = json.loads(self.request.body)
        rainfallReading = RainfallReading(data=data)
        database.insertRainfallReading(rainfallReading)

class MockRainfallHandler(RequestHandler):
    """
    Mock implementation of the Request Handler which returns a 
    simulated set of Rainfall Records
    """
    def get(self, latitude, longitude, start, end):
        records = [] 
        for i in xrange(100):
            record = {
                "timestamp": "201604131602",
                "latitude": random.randint(52000,53000) / float(1000),
                "longitude": random.randint(2000,3000) / float(1000),
                "precipitation": random.randint(0,50)
            }
            records.append(record)

        response = { "rainfall" : [records]}
        self.write(response)
