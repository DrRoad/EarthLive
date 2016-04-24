import sys
from tornado.options import define, options
from tornado.web import Application
from tornado.ioloop import IOLoop
from handlers import VersionHandler, RainfallHandler, MockRainfallHandler, UploadRecordHandler

application = Application([
    (r"/version", VersionHandler),
    (r"/rainfall/(?P<latitude>[0-9o]+)/(?P<longitude>[0-9o]+)/(?P<start>[0-9]+)/(?P<end>[0-9]+)", MockRainfallHandler),
    (r"/upload", UploadRecordHandler)
])
 
if __name__ == "__main__":
	args = sys.argv
	args.append("--log_file_prefix=/opt/logs/eNomad.log")
	options.parse_command_line(args)
	application.listen(8888)
	IOLoop.instance().start()