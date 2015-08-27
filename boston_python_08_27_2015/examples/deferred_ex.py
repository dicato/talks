import json

from twisted.internet import reactor
from twisted.python import log
from twisted.web import client


def gotOrgs(data):
    print("Organization request done!")
    # Parse the JSON payload. TODO Error checking.
    orgs = json.loads(data)
    # Find the names of the organizations and print them.
    org_names = sorted([org['login'] for org in orgs])
    print('\n'.join(org_names))

def shutdown(ignored):
    print("Shutting down!")
    reactor.stop()  # No matter what happens, shutdown the eventloop.

# The Deferred.
d = client.getPage('https://api.github.com/users/clokep/orgs')
d.addCallback(gotOrgs)  # The callback for a successful request.
d.addErrback(log.err)  # Before shutdown, log any errors.
d.addBoth(shutdown)  # The callback/errback.

reactor.run()  # Start the eventloop.
