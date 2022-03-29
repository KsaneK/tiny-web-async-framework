from examples.wsgi_example import app
from tinyweb.constants import ENCODING
from tinyweb.request import Request


def application(environ, start_response):
    request = Request.from_wsgi(environ)
    response = app._handle_request(request=request)

    status = f"{response.status_code.value} {response.status_code.get_name()}"
    start_response(status, list(response.headers.items()))
    yield response.body.encode(ENCODING)
