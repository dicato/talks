import json

from twisted.internet import reactor, task
from twisted.python import log
from twisted.web import resource, server


class ApiResource(resource.Resource):
    def __init__(self, chat_factory, *args, **kwargs):
        # This needs a reference to the NetCatChat factory object.
        self.chat_factory = chat_factory

        resource.Resource.__init__(self, *args, **kwargs)


class Root(ApiResource):
    isLeaf = False

    def __init__(self, *args, **kwargs):
        ApiResource.__init__(self, *args, **kwargs)
        self.putChild('banner', Banner(self.chat_factory))
        self.putChild('users', Users(self.chat_factory))

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


class Banner(ApiResource):
    isLeaf = True

    def _set_banner(self, banner):
        # The json modules returns unicode, we need bytes.
        banner = bytes(banner)
        # Ensure there's a line break at the end.
        if not banner.endswith(b'\r\n'):
            banner += b'\r\n'
        self.chat_factory.banner = banner

    def render_GET(self, request):
        # Get the current banner from the server.
        result = {'banner': self.chat_factory.banner}

        return json.dumps(result, indent=4, separators=(',', ': ')) + "\n"

    def render_POST(self, request):
        status = "ERROR"
        try:
            content = request.content.read()
            data = json.loads(content)['banner']

            # Make this a Deferred so the function can immediately return.
            d = task.deferLater(reactor, 0.1, self._set_banner, data)
            d.addErrback(log.err)

            status = "SUCCESS"
        except ValueError:
            # TODO
            log.err("Unable to parse JSON: %s" % content)
        except KeyError as e:
            # TODO
            log.err("Data does not contain %s" % e.message)

        result = {'status': status}

        return json.dumps(result)


class Users(ApiResource):
    isLeaf = True

    def render_GET(self, request):
        # The user count from server.
        user_count = len(self.chat_factory.clients)
        result = {'users': user_count}

        return json.dumps(result, indent=4, separators=(',', ': ')) + "\n"
