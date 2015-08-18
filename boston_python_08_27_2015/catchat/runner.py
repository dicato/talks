from twisted.internet import reactor, endpoints

from chat import NetCatChatFactory
#from api import ApiFactory

# Create an instance of the factories.
factory = NetCatChatFactory()
#api_factory = ApiFactory()

# Listen on TCP port 1400 for chat and port 80 for the API.
endpoints.serverFromString(reactor, "tcp:1400").listen(factory)
#endpoints.serverFromString(reactor, "tcp:80").listen(api_factory)

# Start listening for connections.
reactor.run()
