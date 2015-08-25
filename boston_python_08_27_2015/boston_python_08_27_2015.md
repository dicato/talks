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
## [fit] learn these *6* concepts

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

## 6. use twisted to build *systems* & *services*

---

## composable & scalable systems

---

## i.e., *service oriented architecture*

---

## i.e., *microservices*

---

# context
## an example app

---

## **chat server** example (with admin dashboard)

- Clients use netcat
- Messages are broadcast to all users
- Clients are sent a banner on login
- Banner is configurable via an admin webpage

---

![fill](images/diagrams.002.png)

---

![fill](images/diagrams.003.png)

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

## [fit] **I/O bound** tasks
## [fit] provides high-level *networking* APIs
## [fit] protocol parsing, handling many non-blocking connections, etc.

---

# [fit] twisted will *not*...

* ...magically make code **non-blocking**
* ...help with CPU-bound tasks<sup>†</sup>
* ...be the simplest library to make a simple HTTP request<sup>‡</sup>

<!--

† Unless you want to coiterate, and also have networking tasks, etc.
‡ Although there is treq: requests built on Twisted

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

<!--

Twisted has event loops that hook into UI event loops (e.g. GTK, wxPython,
win32). Generally, don't change the reactor if you don't need to.

Some functions/methods/classes take in a reactor, this is used for testing and
is not usually provided by client code.

Global singleton: there is only one, ever, it can be accessed everywhere by
importing twisted.internet.reactor.

-->

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

Note that there are a variety of ways to tell a reactor to listen on a port
using a specific protocol.

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

## integrate twisted with other services

---

![fill](images/diagrams.002.png)

---

![fill](images/diagrams.003.png)

---

## admin console
1. current user count
2. set banner/MOTD

---

![fill](images/diagrams.004.png)

---

![fill](images/diagrams.005.png)

---

![fill](images/diagrams.006.png)

---
<!--
Show code here.
-->

```python
import json

from twisted.internet import reactor, task
from twisted.python import log
from twisted.web import resource, server


class ApiResource(resource.Resource):
    # Note that this is available as self.server for every resource.

    def __init__(self, chat_factory, *args, **kwargs):
        # This needs a reference to the NetCatChat factory object.
        self.chat_factory = chat_factory

        resource.Resource.__init__(self, *args, **kwargs)
```

---

```python
class Users(ApiResource):
    isLeaf = True

    def render_GET(self, request):
        # The user count from server.
        user_count = len(self.chat_factory.clients)
        result = {'users': user_count}

        return json.dumps(result, indent=4, separators=(',', ': ')) + "\n"
```

---

```python
class Banner(ApiResource):
    isLeaf = True

    def _set_banner(self, banner):
        # ... error handling ;-)
        self.chat_factory.banner = bytes(banner)  # unicode to bytes

    def render_GET(self, request):
        # Get the banner.
        result = {'banner': self.chat_factory.banner}
        return json.dumps(result, indent=4, separators=(',', ': ')) + "\n"

    def render_POST(self, request):
        # Set the banner.
        status = "ERROR"
        try:
            content = request.content.read()
            data = json.loads(content)['banner']

            # Make this a Deferred so the function can immediately return.
            d = task.deferLater(reactor, 0.1, self._set_banner, data)
            d.addErrback(log.err)

            status = "SUCCESS"
        except Exception:
          # ... error handling ;-)

        return json.dumps({'status': status})
```

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

---

# [fit] Topics we wish we had time for

* trial: testing, the twisted way
* inline callbacks: synchronous-looking deferreds in twisted

<!--

Some topics we didn't really have time for, but this is at least some keywords
to look up!

-->
