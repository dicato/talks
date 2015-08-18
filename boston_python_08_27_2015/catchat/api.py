import json

from twisted.internet import reactor, task, endpoints
from twisted.python import log
from twisted.web import server, resource


BANNER = 'None!'

def get_banner():
    return "MESSAGE OF THE DAY:\n\n + %s\n\n" % BANNER


def set_banner(message):
    global BANNER
    BANNER = message


def get_user_count():
    return 7  # always 7!!


class Root(resource.Resource):
    isLeaf = False

    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild('banner', Banner())
        self.putChild('users', Users())

    def getChild(self, name, request):
        if name == "":
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        return '''<html><body>
        <a href="/banner">Banner</a><br />
        <a href="/users">Users</a><br />
        </body></html>
        '''


class Banner(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        # TODO: Replace get_user_count with actual user count from server.
        result = {'banner': get_banner()}

        return json.dumps(result, indent=4, separators=(',', ': ')) + "\n"

    def render_POST(self, request):
        status = "ERROR"
        try:
            data = json.loads(request.content.read())['banner']

            # Make this a Deferred so the function can immediately return.
            # TODO: Replace print_banner with something that actually sets
            # the banner in the running server.
            d = task.deferLater(reactor, 0.1, set_banner, data)
            d.addErrback(log.err)

            status = "SUCCESS"
        except ValueError:
            # TODO
            log.err("Unable to parse JSON: %s" % request.content.read())
        except KeyError as e:
            # TODO
            log.err("Data does not contain %s" % e.message)

        result = {'status': status}

        return json.dumps(result)


class Users(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        # TODO: Replace get_user_count with actual user count from server.
        result = {'users': get_user_count()}

        return json.dumps(result, indent=4, separators=(',', ': ')) + "\n"

site = server.Site(Root())

if __name__ == "__main__":
    endpoints.serverFromString(reactor, "tcp:8080").listen(site)
    reactor.run()
