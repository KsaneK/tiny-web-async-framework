import asyncio
import traceback
from typing import List

import tinyweb.constants as C
from tinyweb.exceptions import PageNotFoundException
from tinyweb.logger import log, RequestLogger
from tinyweb.request import Request, RequestMethod
from tinyweb.response import Response, StatusCode
from tinyweb.routes import Routes
from tinyweb.utils import generate_error_response


@log(RequestLogger)
class TinyWeb:
    READ_CHUNK_SIZE = 16 * 1024

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

        self._server = None

        self._routes = Routes()

    def run(self):
        self.logger.info(f"Starting webserver on {self._host}:{self._port}...")
        asyncio.run(self._run_server())

    async def _run_server(self):
        self._server = await asyncio.start_server(self._handle_request, self._host, self._port)
        async with self._server:
            await self._server.serve_forever()

    async def _handle_connection(self, reader, writer):
        raw_request = await self._read_http_request_from_stream(reader)

        try:
            request = Request.from_raw_bytes(raw_request=raw_request)
        except Exception:
            traceback.print_exc()
            writer.close()
            return

        response = self._handle_request(request)
        writer.write(response.generate())
        writer.close()

    def _handle_request(self, request):
        try:
            func = self._routes.get_route(request.endpoint, request.method)
            response = Response.from_result(func(request))
        except PageNotFoundException:
            response = generate_error_response(StatusCode.NOT_FOUND)
        except Exception as exc:
            traceback.print_exc()
            response = generate_error_response(StatusCode.INTERNAL_SERVER_ERROR)

        self.logger.log(request=request, status_code=response.status_code.value)

        return response

    @staticmethod
    async def _read_http_request_from_stream(stream) -> str:
        raw_request = ""
        while not raw_request.endswith(2 * C.LINE_END):
            raw_request += (await stream.read(TinyWeb.READ_CHUNK_SIZE)).decode(C.ENCODING)

        return raw_request

    def route(self, path: str, methods: List[str]):
        def decorator(func):
            for method in methods:
                self._routes.add_route(path, RequestMethod(method), func)
            return func

        return decorator
