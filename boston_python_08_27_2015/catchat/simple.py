from twisted.internet import protocol, reactor, endpoints


class BotProtocol(protocol.Protocol):
    # An instance of a Protocol exists for each established connection.

    def connectionMade(self):
        # The connection has been established, perform greetings here.
        pass

    def dataReceived(self, data):
        # ...parse and do something with data...
        pass

    def connectionLost(self, reason):
        # The connection is complete, clean up here.
        pass


class BotFactory(protocol.Factory):
    protocol = BotProtocol
    # The real magic here is the buildProtocol method, but Factory provides a
    # default implementation.


# Create an instance of the factory.
factory = BotFactory()
# Listen on TCP port 1100.
endpoints.serverFromString(reactor, "tcp:1100").listen(factory)
reactor.run()
