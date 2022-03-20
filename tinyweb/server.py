import asyncio
from typing import List

from tinyweb.constants import ENCODING
from tinyweb.exceptions import PageNotFoundException
from tinyweb.request import Request, RequestMethod
from tinyweb.response import Response, StatusCode
from tinyweb.routes import Routes


class TinyWeb:
    READ_CHUNK_SIZE = 16 * 1024

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

        self._server = None
        self._loop = None

        self._routes = Routes()

    def run(self):
        asyncio.run(self._run_server())

    async def _run_server(self):
        self._server = await asyncio.start_server(self._handle_request, self._host, self._port)
        async with self._server:
            await self._server.serve_forever()

    async def _handle_request(self, reader, writer):
        request_raw = ""
        while not request_raw.endswith("\r\n\r\n"):
            request_raw += (await reader.read(TinyWeb.READ_CHUNK_SIZE)).decode(ENCODING)

        try:
            request = Request.parse(raw_request=request_raw)
            func = self._routes.get_route(request.path, request.method)
            response = Response.from_result(func(request))
            writer.write(response.generate())
        except PageNotFoundException:
            writer.write(StatusCode.NOT_FOUND.generate_default_response())
        except Exception:
            writer.write(StatusCode.INTERNAL_SERVER_ERROR.generate_default_response())

        writer.close()

    def route(self, path: str, methods: List[str]):
        def decorator(func):
            for method in methods:
                self._routes.add_route(path, RequestMethod(method), func)
            return func

        return decorator
