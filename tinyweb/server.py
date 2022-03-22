import asyncio
import os
from typing import List

import tinyweb.constants as C
from tinyweb.exceptions import PageNotFoundException
from tinyweb.request import Request, RequestMethod
from tinyweb.response import Response, StatusCode
from tinyweb.routes import Routes
from tinyweb.utils import generate_error_message


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
        while not request_raw.endswith(2 * C.LINE_END):
            request_raw += (await reader.read(TinyWeb.READ_CHUNK_SIZE)).decode(C.ENCODING)

        try:
            request = Request.parse(raw_request=request_raw)
            func = self._routes.get_route(request.path, request.method)
            response = Response.from_result(func(request))
            writer.write(response.generate())
        except PageNotFoundException:
            writer.write(generate_error_message(StatusCode.NOT_FOUND))
        except Exception:
            writer.write(generate_error_message(StatusCode.INTERNAL_SERVER_ERROR))
        writer.close()

    def route(self, path: str, methods: List[str]):
        def decorator(func):
            for method in methods:
                self._routes.add_route(path, RequestMethod(method), func)
            return func

        return decorator
