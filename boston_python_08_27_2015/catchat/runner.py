from twisted.internet import reactor, endpoints
from twisted.web import server

from chat import NetCatChatFactory
from api import Root

# Create an instance of the factories.
factory = NetCatChatFactory()
site = server.Site(Root(factory))

# Listen on TCP port 1400 for chat and port 8080 for the API.
endpoints.serverFromString(reactor, "tcp:1400").listen(factory)
endpoints.serverFromString(reactor, "tcp:8080").listen(site)

# Start listening for connections (and run the event-loop).
reactor.run()
