from twisted.internet import protocol
from twisted.logger import Logger

logger = Logger()


class NetCatChatProtocol(protocol.Protocol):
    # An instance of a Protocol exists for each established connection.

    def connectionMade(self):
        # Called when the protocol is instantiated and the connection is ready.

        # Register to receive messages.
        self.factory.clients.add(self)

        # The connection has been established, perform greetings here.
        self.transport.write(self.factory.banner)

    def dataReceived(self, data):
        # New data (bytes) are available for consuming.

        # Notify the other users of this message.
        logger.info("%s: %s" % (self.transport.getPeer().host, data))
        self.factory.broadcast_message(self, data)

    def connectionLost(self, reason):
        # The connection is about to be terminated.

        # No longer should receive messages.
        self.factory.clients.remove(self)

        # The connection is complete, clean up here.
        self.transport.write(b'Goodbye')

    # Has a transport property for interacting with the connection.

    # Has a factory property for interacting with the factory that build this.


class NetCatChatFactory(protocol.Factory):
    # By defining `protocol`, the default implementation of
    # `Factory.buildProtocol` will work fine!
    protocol = NetCatChatProtocol

    def __init__(self):
        # All the connected chatters.
        self.clients = set()
        # A message to send to each client on connection.
        self.banner = b'Welcome to NetCatChat!\r\n'

    def broadcast_message(self, sender, msg):
        """Send a message to all connected clients."""
        for client in self.clients:
            # Don't resend the data to the sender.
            if client is sender:
                continue
            client.transport.write(msg)
