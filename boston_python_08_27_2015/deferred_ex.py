import json

from twisted.internet import reactor
from twisted.web import client

# The Deferred.
d = client.getPage('https://api.github.com/users/clokep/orgs')

def cbResponse(data):
    # Parse the JSON payload. TODO Error checking.
    orgs = json.loads(data)
    # Find the names of the organizations and print them in
    # alphabetical order.
    org_names = sorted([org['login'] for org in orgs])
    print('\n'.join(org_names))
d.addCallback(cbResponse)  # The callback for a successful request.

def cbShutdown(ignored):
    reactor.stop()  # No matter what happens, shutdown the eventloop.
d.addBoth(cbShutdown)  # The callback/errback.

reactor.run()  # Start the eventloop.
