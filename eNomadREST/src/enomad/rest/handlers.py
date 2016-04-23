'''
Created on 23 Apr 2016

@author: Andy
'''

from datetime import date
from tornado.web import RequestHandler
from enomad.dao.database import RainfallDatabase
 
class VersionHandler(RequestHandler):
    def get(self):
        response = { 'application': 'eNomad',
                     'version': '1.0.2',
                     'last_build':  date.today().isoformat() }
        self.write(response)

class RainfallHandler(RequestHandler)
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
      records = self.database.findRainfallRecords(latitude, longitude,
                                                   start, finish):

      response = { "rainfall" : records }

      self.write(response)


class MockRainfallHandler(RequestHandler):
    """
    Mock implementation of the Request Handler which returns a 
    simulated set of Rainfall Records
    """
    def get(self, latitude, longitude, start, end):
        response = {
            "rainfall" : [
                {
                "timestamp": "201604131602010000",
                "latitude": "52.1111",
                "longitude": "2.6500",
                "precipitation": "21"
              },
              {
                "timestamp": "201604131602020000",
                "latitude": "52.2311",
                "longitude": "2.6500",
                "precipitation": "20"
              },
              {
                "timestamp": "201604131602030000",
                "latitude": "52.6511",
                "longitude": "2.8700",
                "precipitation": "18"
              },
              {
                "timestamp": "201604131602040000",
                "latitude": "52.1111",
                "longitude": "2.4500",
                "precipitation": "25"
              },
              {
                "timestamp": "201604131602050000",
                "latitude": "52.1111",
                "longitude": "2.3000",
                "precipitation": "33"
              }
            ]}
        self.write(response)
