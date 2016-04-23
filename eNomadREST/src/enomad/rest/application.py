from tornado.web import Application
from tornado.ioloop import IOLoop
from handlers import VersionHandler, RainfallHandler, MockRainfallHandler

application = Application([
    (r"/version", VersionHandler)
    (r"/rainfall/(?P<lat>[0-9o]+)/(?P<long>[0-9o]+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)", MockRainfallHandler)
])
 
if __name__ == "__main__":
    application.listen(8888)
    IOLoop.instance().start()