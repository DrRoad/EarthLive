
# NASA Space Apps 2016

## Catching the Rain
We are attempting to link the information from the Global Precipitation Measurement database with Twitter trends so that we can identify flooded areas in realtime and so predict where the floods will occur next. 

### Detecting Floods

## Technology Used

### REST 
Data is retrieved from ... in HDF5 Format.  This is parsed using a Java parser and exported into a JSON file and inserted into the database.

### Databases
#### Riak KV Store

The details of the precipitation are inserted into a Riak NoSql database.  The records are stored in JSON format with a primary key of timestamp | latitude | longitude.
Secondary indexes are added on the latitude and longitude fields individually so that queries can be performed without supplying a date range. 

### Web Front End & Analysis

R
Shiny

