import sys

from twisted.internet import reactor, endpoints
from twisted.logger import Logger
from twisted.python import log
from twisted.web import server

from chat import NetCatChatFactory
from api import Root

# Configure logging to standard out.
logger = Logger()
log.startLogging(sys.stdout)

# Create an instance of the factories.
factory = NetCatChatFactory()
site = server.Site(Root(factory))

# Listen on TCP port 1400 for chat and port 8080 for the API.
endpoints.serverFromString(reactor, "tcp:1400").listen(factory)
endpoints.serverFromString(reactor, "tcp:8080").listen(site)

# Start listening for connections (and run the event-loop).
logger.info("Listening for netcat on port 1400")
logger.info("Listening for HTTP on port 8080")
reactor.run()
