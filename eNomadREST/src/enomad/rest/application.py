from tornado.web import Application
from tornado.ioloop import IOLoop
from handlers import VersionHandler, RainfallHandler, MockRainfallHandler, UploadRecordHandler

application = Application([
    (r"/version", VersionHandler),
    (r"/rainfall/(?P<latitude>[0-9o]+)/(?P<longitude>[0-9o]+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)", MockRainfallHandler)
    (r"/upload", UploadRecordHandler)
])
 
if __name__ == "__main__":
    application.listen(8888)
    IOLoop.instance().start()