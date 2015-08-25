<!---
This is a comment and should not render!
-->

# [fit] twisted
# [fit] _concepts & patterns_

---

# [fit] introduction

---

![right fill](https://avatars0.githubusercontent.com/u/517124?v=3&s=400)

# [fit] Patrick Cloke

## _lead engineer @ Percipient Networks_
## &
## _mozillian_
## @_clokep_

---

![left fill](https://avatars0.githubusercontent.com/u/542728?v=3&s=400)

# [fit] Stephen DiCato

## _co-founder & VP, engineering_
## _@ Percipient Networks_
## @_dicato_

---

### _if you Twitter_
## @clokep & @stephendicato

---

# [fit] expectations
## [fit] learn these *5* concepts

---

## 1. what is twisted

---

## 2. when to use twisted

---
## 3. event loop (reactor)

---

## 4. deferreds

---

## 5. protocols (and more)

---

# [fit] expectations
## [fit] *integrate* twisted

---

## use twisted to build
# [fit] services

---

## **chat server** example (with admin dashboard)

- Clients use netcat
- Messages are broadcast to all users
- Clients are sent a banner on login
- Banner is configurable via an admin webpage

---

(this slide intentionally left blank)

---

## 1. what is twisted

---

## twisted is...
# [fit] **evented** and *asynchronous*
# [fit] networking

<!--

Asynchronous: non-blocking against I/O bound tasks (e.g. reading/writing to
a socket). [Jean-Paul Calderone, http://stackoverflow.com/a/6118510/1070085]

Evented: user code is notified by the event loop when something it cares
about happens (e.g. new data is available on a socket). Frequently layered
in Twisted: e.g. new data to new line to new HTTP request.

-->

---

## example of events (from `chat.py`)

```python
from twisted.internet import protocol


class NetCatChatProtocol(protocol.Protocol):
    def connectionMade(self):
        # Called when the protocol is instantiated and the connection is ready.
        """ ... snipped ... """

    def dataReceived(self, data):
        # New data (bytes) are available for consuming.
        """ ... snipped ... """

    def connectionLost(self, reason):
        # The connection is about to be terminated.
        """ ... snipped ... """
```

---

## 2. when to use twisted

---

## does not magically make code **non-blocking**

TODO

<!--

Why use Twisted?
    * Don't worry about low-level networking
    * Easily handle many connections without blocking
    * Built in parsing of many network protocols.

When shouldn't I use Twisted?
    Twisted will not help you with CPU-bound tasks, e.g. long blocking tasks.

    Twisted is probably not the easiest library if you just want to make an HTTP
    request. (I'd suggest using `requests <http://python-requests.org/>`_.)

-->

---

## 3. event loop (reactor)

---

## [fit] event loop APIs:
### networking, threading, event dispatching, timing, etc.

<!--

The reactor is the Twisted event loop. The reactor provides APIs for networking,
threading, dispatching events, and more.

-->

---

# [fit] reactor depends on
## [fit] *platform* and *other factors*
### reactor is a **global singleton**

---

## example (from `runner.py`)

```python
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
```

<!--

Twisted has event loops that hook into UI event loops (e.g. GTK, wxPython,
win32). Generally, don't change the reactor if you don't need to.

Some functions/methods/classes take in a reactor, this is used for testing and
is not usually provided by client code.

Global singleton: there is only one, ever, it can be accessed everywhere by
importing twisted.internet.reactor.

-->

---

## 4. deferreds

---

## [fit] a **deferred** is a *promise*
## [fit] that a function will eventually have a **result**

<!--

Deferreds are similar to "Promises" or "Futures". They are used to process the
results of an asynchronous function: the function returns (a Deferred)
immediately, callbacks are attached that will received the result of the
previous callback.

-->

---

### in other words...
### deferreds are a *placeholder* for a future *result*

<!--

Would it be worth it to discuss deferreds in the context or something like
celery async results?

-->

---

# [fit] deferreds manage a
## [fit] *callback chain*

<!--
Modified version of http://twistedmatrix.com/documents/current/_images/deferred-process.png
-->
![right 100%](images/deferreds.png)

<!--

The chain of callbacks is processed using the following rules:

1.  Result of the callback is always passed as the first argument to the next
    callback.
2.  If a callback raises an exception, switch to errback.
3.  An unhandled failure gets passed down the line of errbacks, creating an
    asynchronous analog to a series of `except:` statements.
4.  If an errback doesn’t raise an exception or return a
    `twisted.python.failure.Failure` instance, switch to callback.

Deferreds will automatically print a stacktrace when being garbage collected,
it's usually good practice to explicitly add an errback that logs.

See http://twistedmatrix.com/documents/current/core/howto/defer.html

-->

---

## Example (from `deferred_ex.py`)

```python
import json

from twisted.internet import reactor
from twisted.web import client

# The Deferred.
d = client.getPage('https://api.github.com/users/clokep/orgs')

def cbResponse(data):
    orgs = json.loads(data)  # Parse the JSON paload.
    # Find the names of the organizations in alphabetical order.
    org_names = sorted([org['login'] for org in orgs])
    print('\n'.join(org_names))
d.addCallback(cbResponse)  # The callback for a successful request.

def cbShutdown(ignored):
    reactor.stop()  # No matter what happens, shutdown the eventloop.
d.addBoth(cbShutdown)  # The callback/errback.

reactor.run()  # Start the eventloop.
```

---

## Example Deferred flow (from `deferred_ex.py`)

![inline](images/deferred_ex.png)

---

# deferreds fine print

![right 80%](images/deferreds_chains.png)

```python
d = defer.Deferred()
d.addCallback(callback_1)
d.addErrback(errback_1)
d.addCallbacks(callback_2, errback_2)
d.addBoth(cleanup)
```

<!--

Callbacks and errbacks *always* stack with passthrus, adding a callback and an
errback separately don't end up "next" to each other in the callback chain.

-->

---

## 5. protocols (and more)

---

# `Protocols`
## event handlers for a *connection*

* Each new connection gets a new `Protocol` **instance**
* Basic events include:
connection opened/closed, data available
* Transforms wire protocol into higher level events
(e.g. **Line** received or **HTTP request** finished)

<!--

Twisted includes protocol implementations for low-level (e.g. line received) and
high-level protocols (e.g. HTTP, IRC, IMAP). Can easily add custom protocols.

Generally refers to TCP, but similar for UDP: a Protocol is an event handler for
UDP datagrams.

-->

---

## Example (from `chat.py`)

```python
from twisted.internet import protocol


class NetCatChatProtocol(protocol.Protocol):
    # An instance of a Protocol exists for each established connection.

    def connectionMade(self):
        # Called when the protocol is instantiated and the connection is ready.
        """ ... snipped ... """

    def dataReceived(self, data):
        # New data (bytes) are available for consuming.
        """ ... snipped ... """

    def connectionLost(self, reason):
        # The connection is about to be terminated.
        """ ... snipped ... """

    # Has a transport property for interacting with the connection.

    # Has a factory property for interacting with the factory that build this.


class NetCatChatFactory(protocol.Factory):
    """ ... snipped ... See below."""
```

---

# [fit] `ProtocolFactory`
### builds `Protocol` instances
### keeps **state** across `Protocols`

<!--

Twisted provides interfaces (via zope.interfaces) for each of the above objects,
they describe the full API available on each.

Might hold expensive calculations that only need to be done once or
configuration information (e.g. SSH keys, login information), or any shared
state across multiple protocols (e.g. channels on an IRC server).

-->

---

## Example (from `chat.py`)

```python
from twisted.internet import protocol


class NetCatChatProtocol(protocol.Protocol):
    """ ... snipped ... See above."""


class NetCatChatFactory(protocol.Factory):
    # By defining `protocol`, the default implementation of
    # `Factory.buildProtocol` will work fine!
    protocol = NetCatChatProtocol

    """ ... snipped ... """
```

---

# `Transport`

## a way to **send data**

* Write **bytes** to a connection/datagram
* Close a connection
* Query local/remote addresses
* Do not assume *when* data will be sent
* Usually use built-in instances

<!--

Remember that everything in Twisted is bytes not Unicode!

An address varies based on the type of connection: IPv4, IPv6, UNIX, etc.

-->

---

## Example (from `chat.py`)

```python
from twisted.internet import protocol


class NetCatChatProtocol(protocol.Protocol):
    # An instance of a Protocol exists for each established connection.

    def connectionMade(self):
        # Called when the protocol is instantiated and the connection is ready.

        """ ... snipped ..."""

        # The connection has been established, perform greetings here.
        self.transport.write(self.factory.banner)

    def dataReceived(self, data):
        """ ... snipped ..."""

    def connectionLost(self, reason):
        """ ... snipped ..."""

    """ ... snipped ..."""


class NetCatChatFactory(protocol.Factory):
    """ ... snipped ... See above."""
```

---

## trial
# [fit] testing, the twisted way

---

## integrate twisted with other services

---

![fill](images/diagrams.002.png)

---

![fill](images/diagrams.003.png)

---

![fill](images/diagrams.004.png)

---

![fill](images/diagrams.005.png)

---

![fill](images/diagrams.006.png)

---

## What about data *persistence?*
---

![fill 90%](images/diagrams.007.png)

---

![fill 90%](images/diagrams.008.png)

---

1. `twisted.enterprise.adbapi`
2. SQL Alchemy
3. Django ORM
...

### careful not to block!

---

## Is there a better, more reusable way?

---

![fill 80%](images/diagrams.009.png)

---

### How would you *scale* the twisted server?
