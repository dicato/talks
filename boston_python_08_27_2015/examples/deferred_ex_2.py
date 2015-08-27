import json

from twisted.internet import defer, reactor
from twisted.python import log
from twisted.web import client

def gotRepos(data, org):
    """Got the repos for an org, return a tuple of (org name, repos)."""
    print("Got repo information for %s" % org)

    # Parse the JSON payload. TODO Error checking.
    repos = json.loads(data)
    if not repos:  # no repos, return early
        return (org, [])
    # The names of the repos in alphabetical order.
    names = sorted([repo['name'] for repo in repos])
    return (org, names)

def gotOrgs(data):
    print("Organization request done!")
    # Parse the JSON payload. TODO Error checking.
    orgs = json.loads(data)
    # The names of the organizations in alphabetical order.
    org_names = sorted([bytes(org['login']) for org in orgs])

    # Now request the repos under each org.
    ds = []
    for org in org_names:
        print("\t%s" % org)  # print out the org
        d = client.getPage('https://api.github.com/orgs/%s/repos' % org)
        d.addCallback(gotRepos, org)  # pass the org name to the callback.
        ds.append(d)

    # Returning a Deferred causes the next callback to wait.
    return defer.DeferredList(ds)

def printOrgs(org_list):
    print("Outputting repos")
    for success, (org, repos) in org_list:
        print('\t%s: %s' % (org, ', '.join(repos) if repos else '(none)'))

def shutdown(ignored):
    print("Shutting down!")
    reactor.stop()  # No matter what happens, shutdown the eventloop.

# The Deferred.
d = client.getPage('https://api.github.com/users/clokep/orgs')
d.addCallback(gotOrgs)  # The callback for a successful request.
d.addCallback(printOrgs)
d.addErrback(log.err)  # Before shutdown, log any errors.
d.addBoth(shutdown)  # The callback/errback.

reactor.run()  # Start the eventloop.
